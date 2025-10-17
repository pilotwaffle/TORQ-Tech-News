# Claude Code Sub-Agents Reference Guide

## 📚 Source
- Official Documentation: https://docs.claude.com/en/docs/claude-code/sub-agents
- Last Reviewed: October 16, 2025

---

## 🎯 What Are Sub-Agents?

**Sub-agents are specialized AI assistants with specific expertise and purpose:**
- Operate in **separate context windows** from main conversation
- Each has a **unique role and capabilities**
- Can be invoked **automatically or explicitly**
- Have access to **specific tools and models**

### Key Benefits:
- ✅ **Focused expertise** - Each sub-agent specializes in one domain
- ✅ **Clean context** - Fresh context for each invocation
- ✅ **Parallel processing** - Multiple sub-agents can work concurrently
- ✅ **Tool isolation** - Limit tool access per sub-agent
- ✅ **Reusability** - Same sub-agent for multiple projects

---

## 📁 File Structure & Configuration

### File Locations:
```
Project-level (version controlled):
.claude/agents/your-agent.md

User-level (global):
~/.claude/agents/your-agent.md
```

### Configuration Format:
```markdown
---
name: your-sub-agent-name
description: When this subagent should be invoked (used for automatic delegation)
tools: tool1, tool2, tool3  # Optional: comma-separated list
model: sonnet  # Optional: sonnet, opus, haiku
---

# Sub-Agent System Prompt

Your detailed system prompt goes here.
Define the sub-agent's:
- Role and expertise
- Behavior and personality
- Task execution approach
- Output format expectations
```

### Example Sub-Agent Configuration:
```markdown
---
name: code-reviewer
description: Use PROACTIVELY after writing significant code to review for bugs, security issues, and best practices
tools: Read, Grep, Bash
model: sonnet
---

# Expert Code Reviewer

You are an expert code reviewer specializing in:
- Security vulnerabilities
- Performance optimization
- Best practices adherence
- Bug detection

## Review Process:
1. Read the code thoroughly
2. Check for common issues:
   - SQL injection risks
   - XSS vulnerabilities
   - Memory leaks
   - Race conditions
3. Provide actionable recommendations
4. Rate code quality (1-10)

## Output Format:
- 🐛 Bugs Found: [list]
- 🔒 Security Issues: [list]
- ⚡ Performance: [recommendations]
- ✅ Best Practices: [suggestions]
```

---

## 🛠️ Available Tools

### Core Tools:
- **Read** - Read files
- **Write** - Create files
- **Edit** - Modify files
- **Bash** - Execute commands
- **Grep** - Search code
- **Glob** - Find files
- **WebFetch** - Fetch web content
- **WebSearch** - Search the web

### Tool Access Patterns:
```markdown
# Full access to all tools
tools: *

# Specific tools only
tools: Read, Write, Bash

# Read-only access
tools: Read, Grep, Glob

# No tools (prompt-based only)
tools:
```

---

## 🚀 Invocation Methods

### 1. Automatic Delegation (Recommended)
Claude automatically invokes sub-agents based on their `description` field:

```markdown
---
name: database-expert
description: Use PROACTIVELY when user mentions database operations, SQL queries, or data modeling
---
```

**Trigger phrases in description:**
- "Use PROACTIVELY when..."
- "MUST BE USED for..."
- "Automatically invoke when..."

### 2. Explicit Invocation
User or main agent directly requests a specific sub-agent:

```bash
# User types:
/use code-reviewer

# Or main agent uses Task tool:
Task(subagent_type="code-reviewer", prompt="Review the authentication logic")
```

---

## 📋 Best Practices

### Sub-Agent Design:
1. **Single Responsibility**
   - Each sub-agent should have ONE clear purpose
   - ❌ Bad: "general-helper" that does everything
   - ✅ Good: "sql-optimizer" for database query optimization

2. **Clear Descriptions**
   - Use action words: "Use PROACTIVELY when..."
   - Be specific about triggers
   - Include context clues

3. **Tool Minimization**
   - Only grant necessary tools
   - Security through least privilege
   - Reduces token usage

4. **Detailed System Prompts**
   - Define role clearly
   - Specify output format
   - Include examples
   - Set behavior guidelines

### Project Organization:
```
project/
├── .claude/
│   ├── agents/
│   │   ├── deployment-specialist.md    # Deployment tasks
│   │   ├── api-integrator.md           # API integration
│   │   └── data-validator.md           # Data validation
│   └── commands/
│       └── deploy.md                    # Slash commands
```

### Naming Conventions:
- Use kebab-case: `web-scraper-agent.md`
- Be descriptive: `railway-deployment-expert.md`
- Avoid generic names: ❌ `helper.md`, ✅ `database-migration-specialist.md`

---

## 🔄 Communication Patterns

### Main Agent → Sub-Agent:
```python
# Main agent delegates task
Task(
    subagent_type="deployment-expert",
    prompt="Deploy the updated app.py to Railway and verify the deployment succeeded",
    description="Deploy to Railway"
)
```

### Sub-Agent → Main Agent:
- Sub-agent completes task
- Returns final report/summary
- Main agent receives result
- Main agent communicates to user

### Important Notes:
- ⚠️ **One-way communication**: Sub-agents can't ask questions mid-task
- ⚠️ **No context sharing**: Each sub-agent starts fresh
- ⚠️ **Stateless**: No memory between invocations
- ✅ **Detailed prompts**: Include all context needed

---

## 🎨 Sub-Agent Templates

### Template 1: Code Analysis
```markdown
---
name: code-analyzer
description: Use PROACTIVELY to analyze code structure, dependencies, and complexity
tools: Read, Grep, Glob, Bash
model: sonnet
---

# Expert Code Analyzer

Analyze codebases for:
- Architecture patterns
- Dependency graphs
- Code complexity metrics
- Technical debt

Output: Markdown report with visualizations
```

### Template 2: Documentation Writer
```markdown
---
name: doc-writer
description: Use when user requests documentation, README, or API docs
tools: Read, Write, Glob
model: sonnet
---

# Technical Documentation Specialist

Create comprehensive documentation:
- API references
- User guides
- README files
- Code comments

Follow industry standards (Markdown, JSDoc, etc.)
```

### Template 3: Test Generator
```markdown
---
name: test-generator
description: MUST BE USED when writing tests or improving test coverage
tools: Read, Write, Bash
model: sonnet
---

# Test Engineering Expert

Generate comprehensive tests:
- Unit tests
- Integration tests
- Edge cases
- Mocking strategies

Frameworks: Jest, Pytest, Mocha, etc.
```

---

## 🔧 Advanced Features

### Model Selection:
```markdown
# Use faster model for simple tasks
model: haiku

# Use powerful model for complex analysis
model: sonnet

# Use most capable for critical tasks
model: opus
```

### Chaining Sub-Agents:
```python
# Step 1: Code analysis
Task(subagent_type="code-analyzer", ...)

# Step 2: Test generation (uses analysis)
Task(subagent_type="test-generator", ...)

# Step 3: Deployment
Task(subagent_type="deployer", ...)
```

### Conditional Invocation:
```markdown
---
description: Use PROACTIVELY when user mentions 'scraping', 'web data', or 'BeautifulSoup'
---
```

---

## ⚠️ Limitations & Considerations

### Context Isolation:
- Sub-agents don't see main conversation history
- Must include all context in the task prompt
- No access to previous sub-agent outputs

### Token Usage:
- Each sub-agent invocation uses tokens
- System prompts count toward limits
- Consider token budget when designing

### Latency:
- Sub-agent invocation adds slight delay
- Trade-off: specialized expertise vs. speed
- Use for non-trivial tasks

### Error Handling:
- Sub-agents can fail
- Main agent receives error message
- Implement fallback strategies

---

## 📊 Real-World Examples

### Example 1: Web Scraping Agent
```markdown
---
name: ethical-web-scraper
description: Use PROACTIVELY when scraping websites, fetching articles, or automating content collection
tools: Read, Write, Bash, WebFetch
model: sonnet
---

# Ethical Web Scraping Specialist

Expert in:
- BeautifulSoup and Selenium
- robots.txt compliance
- Rate limiting
- Error handling
- Data cleaning

Always follow best practices:
1. Check robots.txt
2. Add delays (2-5s)
3. Set User-Agent
4. Handle errors gracefully
5. Respect terms of service

Output: Clean, validated data in JSON/CSV
```

### Example 2: Railway Deployment Agent
```markdown
---
name: railway-deployment-expert
description: MUST BE USED for Railway deployments, environment variables, or production issues
tools: Read, Bash, Grep
model: sonnet
---

# Railway Deployment Specialist

Handle all Railway operations:
- Deployment troubleshooting
- Environment configuration
- Domain setup
- Database management
- Log analysis

Steps:
1. Verify app configuration
2. Check Railway dashboard
3. Test deployment
4. Monitor logs
5. Validate functionality
```

---

## 🎯 TORQ Tech News Sub-Agent Ideas

### Potential Sub-Agents for This Project:

1. **content-scraper-agent.md**
   - Scrape MIT Sloan articles
   - Clean and validate data
   - Respect robots.txt

2. **railway-ops-agent.md**
   - Deploy to Railway
   - Monitor production
   - Handle errors

3. **analytics-agent.md**
   - Analyze visitor data
   - Generate insights
   - Create dashboards

4. **seo-optimizer-agent.md**
   - Optimize meta tags
   - Improve loading speed
   - Generate sitemaps

5. **security-auditor-agent.md**
   - Check for vulnerabilities
   - Review authentication
   - Test API endpoints

---

## 📚 Additional Resources

- **Official Docs**: https://docs.claude.com/en/docs/claude-code/sub-agents
- **Tool Reference**: https://docs.claude.com/en/docs/claude-code/tools
- **Slash Commands**: https://docs.claude.com/en/docs/claude-code/slash-commands
- **Best Practices**: https://docs.claude.com/en/docs/claude-code/best-practices

---

## ✅ Quick Reference Checklist

When creating a new sub-agent:

- [ ] Choose a descriptive kebab-case name
- [ ] Write clear invocation description
- [ ] Define minimal required tools
- [ ] Select appropriate model
- [ ] Write detailed system prompt
- [ ] Include examples in prompt
- [ ] Specify output format
- [ ] Test with sample tasks
- [ ] Document in project README
- [ ] Version control in .claude/agents/

---

**Last Updated**: October 16, 2025
**Project**: TORQ Tech News
**Status**: Reference document for future sub-agent development
