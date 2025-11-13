"""Azure Table Storage integration for newsletter subscribers.

This module provides a robust subscription management system with Azure Table Storage
as the primary backend and SQLite as a fallback mechanism. It includes email validation,
duplicate detection, and privacy-preserving IP tracking.

Example:
    Basic usage:

    >>> from subscribers_storage import SubscribersStorage
    >>> storage = SubscribersStorage()
    >>> result = storage.subscribe("user@example.com", "192.168.1.1")
    >>> print(result)
    {'success': True, 'message': 'Successfully subscribed!'}

Attributes:
    AZURE_TABLE_NAME (str): Name of the Azure Table for subscribers.
"""

from __future__ import annotations

import hashlib
import logging
import os
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

# Structured logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Azure Table Storage constants
AZURE_TABLE_NAME = "subscribers"
DB_PATH = Path(__file__).parent / "analytics.db"


class SubscriptionError(Exception):
    """Raised when subscription operation fails.

    Attributes:
        message: Human-readable error description.
        code: Error code for client handling.
        status_code: HTTP status code.
        context: Additional error context.
    """

    def __init__(
        self,
        message: str,
        code: str = "SUBSCRIPTION_ERROR",
        status_code: int = 500,
        context: dict[str, Any] | None = None
    ) -> None:
        """Initialize subscription error.

        Args:
            message: Error message.
            code: Error code identifier.
            status_code: HTTP status code to return.
            context: Additional context information.
        """
        self.message = message
        self.code = code
        self.status_code = status_code
        self.context = context or {}
        super().__init__(self.message)


class ValidationError(SubscriptionError):
    """Raised when input validation fails.

    Attributes:
        message: Human-readable error description.
        field: Field that failed validation.
        value: Value that failed validation.
    """

    def __init__(self, message: str, field: str, value: Any) -> None:
        """Initialize validation error.

        Args:
            message: Error message.
            field: Name of the field that failed.
            value: Value that failed validation.
        """
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=400,
            context={"field": field, "value": str(value)}
        )


class DuplicateSubscriptionError(SubscriptionError):
    """Raised when email is already subscribed.

    Attributes:
        email: Email address that is already subscribed.
    """

    def __init__(self, email: str) -> None:
        """Initialize duplicate subscription error.

        Args:
            email: Email address that's already subscribed.
        """
        super().__init__(
            message="Email already subscribed",
            code="DUPLICATE_EMAIL",
            status_code=409,
            context={"email": email}
        )


@dataclass(frozen=True)
class SubscriptionResult:
    """Represents subscription operation result.

    Attributes:
        success: Whether the operation was successful.
        message: Human-readable message.
        email: Email address that was subscribed.
        timestamp: When the subscription occurred.
        storage_backend: Which backend was used (azure/sqlite).
    """
    success: bool
    message: str
    email: str
    timestamp: str
    storage_backend: str


class SubscribersStorage:
    """Manages subscriber data with Azure Table Storage and SQLite fallback.

    This class provides a unified interface for managing newsletter subscriptions
    with automatic fallback from Azure Table Storage to SQLite if Azure is unavailable.

    Attributes:
        table_client: Azure Table Storage client (if available).
        use_azure: Whether Azure Table Storage is available.

    Example:
        >>> storage = SubscribersStorage()
        >>> result = storage.subscribe("user@example.com", "192.168.1.1")
        >>> if result.success:
        ...     print(f"Subscribed with {result.storage_backend}")
    """

    # Email validation regex (RFC 5322 simplified)
    EMAIL_REGEX = re.compile(
        r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}'
        r'[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
    )

    def __init__(self) -> None:
        """Initialize subscribers storage with Azure and SQLite backends.

        Attempts to connect to Azure Table Storage first. If unavailable,
        falls back to SQLite. Always initializes SQLite as backup.

        Raises:
            SubscriptionError: If both Azure and SQLite initialization fail.
        """
        self.table_client = None
        self.use_azure = False

        # Try to initialize Azure Table Storage
        self._init_azure_storage()

        # Always initialize SQLite as fallback
        self._init_sqlite_storage()

        logger.info(
            "SubscribersStorage initialized",
            extra={
                "azure_available": self.use_azure,
                "sqlite_path": str(DB_PATH)
            }
        )

    def _init_azure_storage(self) -> None:
        """Initialize Azure Table Storage client.

        Reads connection string from AZURE_STORAGE_CONNECTION_STRING environment
        variable. If not set or invalid, logs warning and continues without Azure.
        """
        connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')

        if not connection_string:
            logger.warning(
                "Azure connection string not found, using SQLite fallback",
                extra={"env_var": "AZURE_STORAGE_CONNECTION_STRING"}
            )
            return

        try:
            from azure.data.tables import TableServiceClient
            from azure.core.exceptions import AzureError

            # Create table service client
            service_client = TableServiceClient.from_connection_string(
                conn_str=connection_string
            )

            # Create table if it doesn't exist
            try:
                service_client.create_table(AZURE_TABLE_NAME)
                logger.info(f"Created Azure table: {AZURE_TABLE_NAME}")
            except AzureError:
                # Table already exists
                logger.info(f"Using existing Azure table: {AZURE_TABLE_NAME}")

            # Get table client
            self.table_client = service_client.get_table_client(AZURE_TABLE_NAME)
            self.use_azure = True

            logger.info(
                "Azure Table Storage connected successfully",
                extra={"table": AZURE_TABLE_NAME}
            )

        except ImportError:
            logger.error(
                "azure-data-tables package not installed",
                extra={"solution": "pip install azure-data-tables"}
            )
        except Exception as e:
            logger.error(
                "Failed to initialize Azure Table Storage",
                extra={"error": str(e), "error_type": type(e).__name__},
                exc_info=True
            )

    def _init_sqlite_storage(self) -> None:
        """Initialize SQLite database for subscribers.

        Creates subscribers table if it doesn't exist with proper schema
        for email, subscription date, status, and IP hash.

        Raises:
            SubscriptionError: If SQLite database cannot be initialized.
        """
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS subscribers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    email_domain TEXT NOT NULL,
                    subscribed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    source TEXT DEFAULT 'torqtechnews',
                    status TEXT DEFAULT 'active',
                    ip_hash TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create indexes for performance
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_subscribers_email
                ON subscribers(email)
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_subscribers_status
                ON subscribers(status)
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_subscribers_domain
                ON subscribers(email_domain)
            ''')

            conn.commit()
            conn.close()

            logger.info(
                "SQLite subscribers table initialized",
                extra={"db_path": str(DB_PATH)}
            )

        except sqlite3.Error as e:
            logger.critical(
                "Failed to initialize SQLite database",
                extra={"error": str(e)},
                exc_info=True
            )
            raise SubscriptionError(
                "Database initialization failed",
                code="DB_INIT_ERROR",
                status_code=500,
                context={"error": str(e)}
            ) from e

    def validate_email(self, email: str) -> str:
        """Validate and normalize email address.

        Args:
            email: Email address to validate.

        Returns:
            Normalized email address (lowercase, stripped).

        Raises:
            ValidationError: If email format is invalid.

        Example:
            >>> storage = SubscribersStorage()
            >>> email = storage.validate_email("  User@Example.COM  ")
            >>> print(email)
            user@example.com
        """
        if not email:
            raise ValidationError(
                "Email address is required",
                field="email",
                value=email
            )

        # Normalize: strip whitespace and lowercase
        email_normalized = email.strip().lower()

        # Validate format
        if not self.EMAIL_REGEX.match(email_normalized):
            raise ValidationError(
                "Invalid email format",
                field="email",
                value=email
            )

        # Length validation
        if len(email_normalized) > 254:
            raise ValidationError(
                "Email address too long (max 254 characters)",
                field="email",
                value=email
            )

        return email_normalized

    def hash_ip(self, ip_address: str) -> str:
        """Hash IP address for privacy preservation.

        Uses SHA-256 with truncation to 16 characters for storage efficiency
        while maintaining reasonable uniqueness.

        Args:
            ip_address: IP address to hash.

        Returns:
            Hashed IP address (16 character hex string).

        Example:
            >>> storage = SubscribersStorage()
            >>> hashed = storage.hash_ip("192.168.1.1")
            >>> len(hashed)
            16
        """
        return hashlib.sha256(ip_address.encode()).hexdigest()[:16]

    def extract_domain(self, email: str) -> str:
        """Extract domain from email address.

        Used as partition key in Azure Table Storage for efficient querying
        and distribution.

        Args:
            email: Email address.

        Returns:
            Domain portion of email (e.g., "gmail.com").

        Example:
            >>> storage = SubscribersStorage()
            >>> domain = storage.extract_domain("user@example.com")
            >>> print(domain)
            example.com
        """
        return email.split('@')[1]

    def _subscribe_azure(
        self,
        email: str,
        ip_hash: str,
        timestamp: str
    ) -> None:
        """Subscribe email using Azure Table Storage.

        Args:
            email: Validated email address.
            ip_hash: Hashed IP address.
            timestamp: ISO format timestamp.

        Raises:
            DuplicateSubscriptionError: If email already exists.
            SubscriptionError: If Azure operation fails.
        """
        if not self.table_client:
            raise SubscriptionError(
                "Azure Table Storage not available",
                code="AZURE_UNAVAILABLE",
                status_code=503
            )

        try:
            from azure.core.exceptions import ResourceExistsError

            domain = self.extract_domain(email)

            # Check if already subscribed
            try:
                entity = self.table_client.get_entity(
                    partition_key=domain,
                    row_key=email
                )
                if entity.get('status') == 'active':
                    raise DuplicateSubscriptionError(email)
            except Exception:
                # Entity doesn't exist, continue with subscription
                pass

            # Create entity
            entity = {
                'PartitionKey': domain,
                'RowKey': email,
                'email': email,
                'email_domain': domain,
                'subscribed_at': timestamp,
                'source': 'torqtechnews',
                'status': 'active',
                'ip_hash': ip_hash
            }

            self.table_client.create_entity(entity=entity)

            logger.info(
                "Subscriber added to Azure Table Storage",
                extra={
                    "email_domain": domain,
                    "timestamp": timestamp
                }
            )

        except ResourceExistsError:
            raise DuplicateSubscriptionError(email)
        except DuplicateSubscriptionError:
            raise
        except Exception as e:
            logger.error(
                "Azure subscription failed",
                extra={"error": str(e)},
                exc_info=True
            )
            raise SubscriptionError(
                "Failed to save subscription to Azure",
                code="AZURE_SAVE_ERROR",
                status_code=500,
                context={"error": str(e)}
            ) from e

    def _subscribe_sqlite(
        self,
        email: str,
        ip_hash: str,
        timestamp: str
    ) -> None:
        """Subscribe email using SQLite database.

        Args:
            email: Validated email address.
            ip_hash: Hashed IP address.
            timestamp: ISO format timestamp.

        Raises:
            DuplicateSubscriptionError: If email already exists.
            SubscriptionError: If database operation fails.
        """
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            domain = self.extract_domain(email)

            # Check for existing subscription
            cursor.execute(
                'SELECT status FROM subscribers WHERE email = ?',
                (email,)
            )
            result = cursor.fetchone()

            if result:
                if result[0] == 'active':
                    conn.close()
                    raise DuplicateSubscriptionError(email)
                else:
                    # Reactivate unsubscribed email
                    cursor.execute(
                        '''UPDATE subscribers
                        SET status = 'active',
                            subscribed_at = ?,
                            ip_hash = ?,
                            updated_at = ?
                        WHERE email = ?''',
                        (timestamp, ip_hash, timestamp, email)
                    )
            else:
                # Insert new subscriber
                cursor.execute(
                    '''INSERT INTO subscribers
                    (email, email_domain, subscribed_at, source, status, ip_hash)
                    VALUES (?, ?, ?, 'torqtechnews', 'active', ?)''',
                    (email, domain, timestamp, ip_hash)
                )

            conn.commit()
            conn.close()

            logger.info(
                "Subscriber added to SQLite database",
                extra={
                    "email_domain": domain,
                    "timestamp": timestamp
                }
            )

        except sqlite3.IntegrityError:
            raise DuplicateSubscriptionError(email)
        except DuplicateSubscriptionError:
            raise
        except sqlite3.Error as e:
            logger.error(
                "SQLite subscription failed",
                extra={"error": str(e)},
                exc_info=True
            )
            raise SubscriptionError(
                "Failed to save subscription to database",
                code="DB_SAVE_ERROR",
                status_code=500,
                context={"error": str(e)}
            ) from e

    def subscribe(
        self,
        email: str,
        ip_address: str | None = None
    ) -> SubscriptionResult:
        """Subscribe an email address to the newsletter.

        Validates email, checks for duplicates, and saves to Azure Table Storage
        with automatic fallback to SQLite if Azure is unavailable.

        Args:
            email: Email address to subscribe.
            ip_address: IP address of subscriber (optional, for analytics).

        Returns:
            SubscriptionResult with operation details.

        Raises:
            ValidationError: If email format is invalid.
            DuplicateSubscriptionError: If email already subscribed.
            SubscriptionError: If subscription operation fails.

        Example:
            >>> storage = SubscribersStorage()
            >>> result = storage.subscribe("user@example.com", "192.168.1.1")
            >>> print(result.success)
            True
        """
        # Validate email
        email_normalized = self.validate_email(email)

        # Hash IP for privacy
        ip_hash = self.hash_ip(ip_address) if ip_address else "unknown"

        # Current timestamp
        timestamp = datetime.utcnow().isoformat()

        # Try Azure first, fallback to SQLite
        backend = "sqlite"
        if self.use_azure:
            try:
                self._subscribe_azure(email_normalized, ip_hash, timestamp)
                backend = "azure"
            except (DuplicateSubscriptionError, ValidationError):
                raise
            except Exception as e:
                logger.warning(
                    "Azure subscription failed, falling back to SQLite",
                    extra={"error": str(e)}
                )
                self._subscribe_sqlite(email_normalized, ip_hash, timestamp)
        else:
            self._subscribe_sqlite(email_normalized, ip_hash, timestamp)

        return SubscriptionResult(
            success=True,
            message="Successfully subscribed!",
            email=email_normalized,
            timestamp=timestamp,
            storage_backend=backend
        )

    def get_subscriber_count(self) -> dict[str, Any]:
        """Get total subscriber count from available backend.

        Returns:
            Dictionary with count and backend information.

        Example:
            >>> storage = SubscribersStorage()
            >>> stats = storage.get_subscriber_count()
            >>> print(f"Total: {stats['count']} via {stats['backend']}")
        """
        if self.use_azure:
            try:
                # Query Azure Table Storage
                entities = list(self.table_client.query_entities(
                    query_filter="status eq 'active'"
                ))
                return {
                    'count': len(entities),
                    'backend': 'azure',
                    'success': True
                }
            except Exception as e:
                logger.error(
                    "Failed to count Azure subscribers",
                    extra={"error": str(e)}
                )

        # Fallback to SQLite
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM subscribers WHERE status = 'active'"
            )
            count = cursor.fetchone()[0]
            conn.close()

            return {
                'count': count,
                'backend': 'sqlite',
                'success': True
            }
        except sqlite3.Error as e:
            logger.error(
                "Failed to count SQLite subscribers",
                extra={"error": str(e)}
            )
            return {
                'count': 0,
                'backend': 'error',
                'success': False,
                'error': str(e)
            }
