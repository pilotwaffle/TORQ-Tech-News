# 🎥 Analytics Tool Video Demonstration

This demonstration shows the TORQ Tech News Analytics Tool in action.

## 📹 Demo Script

The `create_demo_video.py` script provides an interactive demonstration of the analytics tool:

```bash
python create_demo_video.py
```

## 🎬 What the Demo Shows

### Step 1: Help & Usage
Shows all available command-line options and usage examples.

### Step 2: Test Data Generation
Creates a sample database with 100 realistic sessions across multiple:
- Days (last 7 days)
- Devices (desktop, mobile, tablet)
- Browsers (Chrome, Firefox, Safari, Edge)
- Traffic sources (Google, Twitter, LinkedIn, direct)

### Step 3: Analytics Report
Generates a comprehensive report showing:
- **Visitor Statistics**: 100 unique visitors, 183 page views, 17% bounce rate
- **Top Articles**: Most viewed content ranked by popularity
- **Conversion Funnel**: 83% homepage→article rate, 44.58% completion rate
- **Hourly Activity**: Visual bar chart of traffic patterns

### Step 4: JSON Export
Demonstrates exporting analytics to JSON format for:
- Dashboard integration
- Business intelligence tools
- Custom visualizations

## 📊 Sample Output

```
======================================================================
TORQ Tech News - Analytics Report (Last 7 Days)
======================================================================

[1] VISITOR STATISTICS
----------------------------------------------------------------------
  Unique Visitors:       100
  Total Page Views:      183
  Active Sessions:       0
  Avg Session Duration:  317.9 seconds
  Bounce Rate:           17.00%

[6] CONVERSION FUNNEL ANALYSIS
----------------------------------------------------------------------
  Homepage Visits:                100
  Article Views:                  83
  
  Homepage → Article Rate:        83.00%
  Article Completion Rate:        44.58%
  External Click Rate:            25.30%

[9] HOURLY ACTIVITY PATTERN
----------------------------------------------------------------------
  00:00  ███████████████                  7
  06:00  ████████████████████            8
  12:00  ████████████████████████       10
  18:00  ██████████████████              7
```

## 🚀 Try It Yourself

```bash
# Run the demo
python create_demo_video.py

# Or test the actual tool with sample data
python test_analyze.py

# Or run analysis on your own database
python analyze_data.py --days 30 --export report.json
```

## 📁 Output Files

The demonstration creates:
- `test_analytics.db` - Sample SQLite database with test data
- `test_report.json` - JSON export of analytics
- `demo_report.json` - Additional JSON export example
- `demonstration_output.txt` - Full demonstration output

## 📖 Learn More

- **Full Documentation**: [ANALYTICS_TOOL_README.md](ANALYTICS_TOOL_README.md)
- **Quick Reference**: [ANALYTICS_QUICK_REF.md](ANALYTICS_QUICK_REF.md)
- **Implementation Details**: [ANALYTICS_IMPLEMENTATION.md](ANALYTICS_IMPLEMENTATION.md)

---

**Created**: 2025-11-01
**Tool Version**: 1.0.0
