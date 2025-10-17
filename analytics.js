/**
 * TORQ Tech News - Advanced Analytics Tracking Script
 *
 * Privacy-focused, performance-optimized client-side analytics
 * Tracks: scroll depth, time on page, clicks, user engagement, session lifecycle
 *
 * Features:
 * - Batched event sending (reduces server load)
 * - Debounced scroll tracking
 * - Session management with localStorage
 * - Non-blocking (doesn't affect page load)
 * - Error handling with fallback
 */

(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        BATCH_SIZE: 5,
        BATCH_TIMEOUT: 10000, // 10 seconds
        TIME_INTERVAL: 30000, // 30 seconds
        SCROLL_DEBOUNCE: 500, // 500ms
        SESSION_TIMEOUT: 1800000, // 30 minutes
        ENDPOINTS: {
            TRACK_EVENT: '/api/track-event',
            TRACK_SESSION: '/api/track-session'
        }
    };

    // State
    const state = {
        sessionId: null,
        eventQueue: [],
        batchTimer: null,
        timeOnPage: 0,
        scrollDepths: new Set(),
        sessionStartTime: null,
        lastActivityTime: null,
        isActive: true
    };

    // Utility: Get or create session ID
    function getSessionId() {
        if (state.sessionId) return state.sessionId;

        // Try cookie first
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'session_id') {
                state.sessionId = value;
                return value;
            }
        }

        // Try localStorage
        const stored = localStorage.getItem('torq_session_id');
        const storedTime = localStorage.getItem('torq_session_time');

        if (stored && storedTime) {
            const elapsed = Date.now() - parseInt(storedTime, 10);
            if (elapsed < CONFIG.SESSION_TIMEOUT) {
                state.sessionId = stored;
                return stored;
            }
        }

        // Create new session ID
        const newSessionId = generateSessionId();
        state.sessionId = newSessionId;
        localStorage.setItem('torq_session_id', newSessionId);
        localStorage.setItem('torq_session_time', Date.now().toString());

        return newSessionId;
    }

    // Utility: Generate unique session ID
    function generateSessionId() {
        return 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // Utility: Get current page URL
    function getCurrentPage() {
        return window.location.pathname;
    }

    // Utility: Get screen resolution
    function getScreenResolution() {
        return `${window.screen.width}x${window.screen.height}`;
    }

    // Utility: Debounce function
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Utility: Safe fetch with error handling
    async function safeFetch(url, options) {
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });
            return response.ok;
        } catch (error) {
            console.warn('[Analytics] Tracking request failed:', error);
            return false;
        }
    }

    // Event Queue: Add event to queue
    function queueEvent(eventType, elementId = '', value = '') {
        const event = {
            session_id: getSessionId(),
            event_type: eventType,
            element_id: elementId,
            value: value,
            page_url: getCurrentPage(),
            timestamp: new Date().toISOString()
        };

        state.eventQueue.push(event);

        // Send batch if queue is full
        if (state.eventQueue.length >= CONFIG.BATCH_SIZE) {
            sendBatch();
        } else {
            // Set timer to send batch after timeout
            if (!state.batchTimer) {
                state.batchTimer = setTimeout(sendBatch, CONFIG.BATCH_TIMEOUT);
            }
        }
    }

    // Event Queue: Send batch of events
    async function sendBatch() {
        if (state.eventQueue.length === 0) return;

        clearTimeout(state.batchTimer);
        state.batchTimer = null;

        const batch = [...state.eventQueue];
        state.eventQueue = [];

        // Send each event (could be optimized to send as bulk in future)
        for (const event of batch) {
            await safeFetch(CONFIG.ENDPOINTS.TRACK_EVENT, {
                method: 'POST',
                body: JSON.stringify(event)
            });
        }
    }

    // Session Management: Update session
    async function updateSession(action = 'update') {
        const duration = Math.floor((Date.now() - state.sessionStartTime) / 1000);

        await safeFetch(CONFIG.ENDPOINTS.TRACK_SESSION, {
            method: 'POST',
            body: JSON.stringify({
                session_id: getSessionId(),
                action: action,
                duration: duration,
                screen_resolution: getScreenResolution()
            })
        });
    }

    // Tracking: Scroll depth
    const trackScroll = debounce(function() {
        const scrollPercentage = Math.round(
            ((window.scrollY + window.innerHeight) / document.documentElement.scrollHeight) * 100
        );

        const thresholds = [25, 50, 75, 100];
        for (const threshold of thresholds) {
            if (scrollPercentage >= threshold && !state.scrollDepths.has(threshold)) {
                state.scrollDepths.add(threshold);
                queueEvent('scroll_depth', 'page', threshold.toString());
            }
        }
    }, CONFIG.SCROLL_DEBOUNCE);

    // Tracking: Time on page
    function trackTimeOnPage() {
        state.timeOnPage += CONFIG.TIME_INTERVAL / 1000;
        queueEvent('time_on_page', 'page', state.timeOnPage.toString());
    }

    // Tracking: Click events
    function trackClick(event) {
        const target = event.target;
        const tagName = target.tagName.toLowerCase();

        // Track link clicks
        if (tagName === 'a') {
            const href = target.href || '';
            const isExternal = href && (
                href.startsWith('http') &&
                !href.includes(window.location.hostname)
            );

            if (isExternal) {
                queueEvent('outbound_link', target.id || 'external_link', href);
            } else {
                queueEvent('internal_link', target.id || 'internal_link', href);
            }
        }

        // Track button clicks
        else if (tagName === 'button' || target.classList.contains('btn')) {
            queueEvent('button_click', target.id || target.className, target.textContent.trim().substring(0, 50));
        }
    }

    // Tracking: User engagement (active vs passive)
    function trackActivity() {
        state.lastActivityTime = Date.now();

        if (!state.isActive) {
            state.isActive = true;
            queueEvent('user_active', 'activity', 'resumed');
        }
    }

    function checkInactivity() {
        const inactiveTime = Date.now() - state.lastActivityTime;

        if (inactiveTime > 60000 && state.isActive) { // 1 minute
            state.isActive = false;
            queueEvent('user_inactive', 'activity', 'paused');
        }
    }

    // Tracking: Article completion (if reading time element exists)
    function trackArticleCompletion() {
        const readingTimeEl = document.querySelector('[data-reading-time]');
        if (!readingTimeEl) return;

        const estimatedReadTime = parseInt(readingTimeEl.dataset.readingTime, 10) || 5;
        const actualTime = state.timeOnPage;

        // If user spent >= 70% of estimated read time, consider article "read"
        if (actualTime >= (estimatedReadTime * 60 * 0.7)) {
            queueEvent('article_complete', 'article', estimatedReadTime.toString());
        }
    }

    // Session: Initialize
    function initSession() {
        state.sessionId = getSessionId();
        state.sessionStartTime = Date.now();
        state.lastActivityTime = Date.now();

        // Update session start
        updateSession('start');
    }

    // Session: End
    async function endSession() {
        await updateSession('end');
        await sendBatch(); // Send any remaining events
    }

    // Event Listeners: Setup
    function setupEventListeners() {
        // Scroll tracking
        window.addEventListener('scroll', trackScroll, { passive: true });

        // Click tracking
        document.addEventListener('click', trackClick, { passive: true });

        // Activity tracking
        ['mousemove', 'keydown', 'scroll', 'touchstart'].forEach(event => {
            document.addEventListener(event, trackActivity, { passive: true });
        });

        // Visibility change (tab switching)
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                queueEvent('tab_hidden', 'visibility', 'hidden');
                sendBatch(); // Send events before tab might close
            } else {
                queueEvent('tab_visible', 'visibility', 'visible');
            }
        });

        // Page unload
        window.addEventListener('beforeunload', () => {
            endSession();
        });

        // Page show (back/forward cache)
        window.addEventListener('pageshow', (event) => {
            if (event.persisted) {
                queueEvent('page_restore', 'bfcache', 'restored');
            }
        });
    }

    // Timers: Setup
    function setupTimers() {
        // Time on page tracking
        setInterval(() => {
            trackTimeOnPage();
            checkInactivity();
            trackArticleCompletion();
        }, CONFIG.TIME_INTERVAL);

        // Session update
        setInterval(() => {
            updateSession('update');
        }, 60000); // Every minute
    }

    // Initialize analytics
    function init() {
        // Don't track if DNT is enabled
        if (navigator.doNotTrack === '1' || window.doNotTrack === '1') {
            console.log('[Analytics] Do Not Track enabled, analytics disabled');
            return;
        }

        // Don't track in development
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            console.log('[Analytics] Development mode, tracking reduced');
        }

        try {
            initSession();
            setupEventListeners();
            setupTimers();

            // Track initial page view
            queueEvent('page_view', 'initial', getCurrentPage());

            console.log('[Analytics] Tracking initialized');
        } catch (error) {
            console.error('[Analytics] Initialization error:', error);
        }
    }

    // Start when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose API for manual tracking (optional)
    window.TORQAnalytics = {
        trackEvent: queueEvent,
        updateSession: updateSession,
        getSessionId: getSessionId
    };

})();
