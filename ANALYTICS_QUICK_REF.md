# Analytics Tool - Quick Reference

## Basic Commands

```bash
# View analytics for last 7 days (default)
python analyze_data.py

# View analytics for last 30 days
python analyze_data.py --days 30

# Export to JSON file
python analyze_data.py --export report.json

# Simple report (no hourly breakdown)
python analyze_data.py --simple

# Test the tool with sample data
python test_analyze.py
```

## What You Get

### 1. Visitor Stats
- Unique visitors
- Total page views
- Active sessions
- Average session duration
- Bounce rate

### 2. Top Articles
List of most viewed articles with view counts

### 3. Traffic Sources
Where your visitors come from (Google, Twitter, direct, etc.)

### 4. Device Breakdown
Desktop vs Mobile vs Tablet usage percentages

### 5. Browser Stats
Which browsers your visitors use

### 6. Conversion Funnel
- Homepage visits → Article views
- Article completion rate (scroll to bottom)
- External link click rate

### 7. User Engagement
- Average scroll depth
- Average time on page
- Total clicks

### 8. Content Stats
- Total articles
- Articles with full text
- Content sources used
- Last update time

### 9. Hourly Activity
Visual bar chart showing peak traffic times

### 10. Recent Activity
Latest visitor sessions and pages viewed

## Common Use Cases

### Daily Monitoring
```bash
python analyze_data.py --days 1
```

### Weekly Report
```bash
python analyze_data.py --days 7 --export weekly_report.json
```

### Monthly Review
```bash
python analyze_data.py --days 30 --export monthly_report.json
```

## Pro Tips

1. **Run regularly**: Schedule daily reports to track trends
2. **Compare periods**: Export multiple reports to compare weeks/months
3. **Watch bounce rate**: High bounce rate (>50%) means users aren't engaging
4. **Track peak hours**: Use hourly activity to schedule content updates
5. **Monitor sources**: Focus marketing on top-performing referrers

## Getting Help

```bash
python analyze_data.py --help
```

See [ANALYTICS_TOOL_README.md](ANALYTICS_TOOL_README.md) for full documentation.
