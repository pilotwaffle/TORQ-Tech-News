# MIT Sloan Management Review - Design Reference

## Official Color Palette

### Primary Colors
- **MIT Sloan Blue**: `#005b9c` (Primary brand color)
- **MIT Sloan Blue Dark**: `#004875` (Hover states, dark variants)
- **Cyan Accent**: `#00e0ff` (Secondary accent)
- **Red Accent**: `#ed1b2e` (Alert, important highlights)
- **MIT Red**: `#A31F34` (Secondary brand color)

### Neutral Colors
- **Background**: `#ffffff` (White)
- **Text Primary**: `#000000` (Black)
- **Text Secondary**: `#f0f0f0` (Silver/Gray)

## Typography

### Font Families
- **Primary Body**: `freight-sans-pro` or `Inter` (fallback)
- **Headings**: `guyot-headline` or `Inter` (fallback)

### Font Sizes
- **Body Text**: `1.125rem` (18px)
- **Large Heading**: `4.99995rem`
- **H1**: `3.35925rem`
- **H2**: `2.799rem`
- **Article Title**: `1.35rem` (bold)
- **Article Description**: `0.937125rem`

### Font Weights
- Light: 300
- Regular: 400
- Medium: 500
- Semibold: 600
- Bold: 700
- Extrabold: 800

## Layout Structure

### Container
- **Max Width**: `1500px`
- **Responsive Padding**: `1.5rem` (mobile), `2rem` (desktop)

### Header
- **Height**: `92px` (fixed)
- **Position**: Fixed at top
- **Background**: White with bottom border
- **Shadow**: Subtle (`0 1px 2px rgba(0,0,0,0.05)`)

### Grid Systems
- **Mobile**: 1 column
- **Tablet** (640px+): 2 columns
- **Desktop** (1024px+): 3 columns

## Component Styles

### Article Cards
- **Border Radius**: `12px`
- **Image Height**: `200px`
- **Shadow**: `0 4px 6px rgba(0,0,0,0.07)`
- **Hover Shadow**: `0 20px 25px rgba(0,0,0,0.15)`
- **Hover Transform**: `translateY(-8px)`

### Category Badges
- **Technology**: `#2196F3` (Blue)
- **Leadership**: `#9C27B0` (Purple)
- **Strategy**: `#607D8B` (Blue Gray)
- **Innovation**: `#E91E63` (Pink)
- **Sustainability**: `#4CAF50` (Green)
- **Finance**: `#FF9800` (Orange)

### Transitions
- **Fast**: `150ms ease`
- **Base**: `250ms ease`
- **Slow**: `350ms ease`

## Design Principles

### 1. Professional & Clean
- Ample whitespace
- Clear hierarchy
- Minimalist approach
- Focus on content readability

### 2. Responsive Design
- Mobile-first approach
- Flexible grid systems
- Touch-friendly interfaces
- Optimized for all screen sizes

### 3. Accessibility
- High contrast ratios
- Semantic HTML
- Focus states for keyboard navigation
- ARIA labels where needed

### 4. Performance
- Optimized images
- Minimal animations
- Efficient CSS
- Fast page loads

## Automation Agent Guidelines

### Content Fetching
1. **Article Structure**:
   - Title (max 100 characters)
   - Excerpt (max 200 characters)
   - High-quality image (800x600 minimum)
   - Category from predefined list
   - Author name (format: "Dr./Prof. FirstName LastName")
   - Reading time (5-15 minutes)

2. **Image Requirements**:
   - Use Unsplash API with specific photo IDs
   - Format: `https://images.unsplash.com/photo-{ID}?w=800&h=600&fit=crop`
   - Business/professional themes
   - High quality, well-composed

3. **Content Quality**:
   - Professional academic tone
   - Research-backed insights
   - Practical business applications
   - Clear, concise writing

### Maintaining Design Consistency

1. **Color Usage**:
   - Primary actions: MIT Sloan Blue
   - Warnings/alerts: Red Accent
   - Success states: Green (`#4CAF50`)
   - Information: Cyan Accent

2. **Spacing**:
   - Section padding: `6rem` (96px)
   - Element spacing: `2rem` (32px)
   - Card gaps: `1.5rem` (24px)
   - Content padding: `1rem` (16px)

3. **Typography Scale**:
   - Hero title: `3rem` (48px)
   - Section titles: `2.5rem` (40px)
   - Article titles: `1.25rem` (20px)
   - Body text: `1.125rem` (18px)
   - Small text: `0.875rem` (14px)

## Update Frequency

### Automation Schedule
- **Content Updates**: Every 1 hour
- **Image Refresh**: When content updates
- **Analytics Check**: Real-time
- **Design Consistency**: Validate on each update

### Quality Checks
- ✅ All images load successfully
- ✅ Color scheme matches reference
- ✅ Typography is consistent
- ✅ Responsive breakpoints work
- ✅ Hover states function correctly
- ✅ Links are valid and functional

## Reference Sites
- **Official Site**: https://sloanreview.mit.edu/
- **Color Picker**: Use browser dev tools to verify colors
- **Typography**: Inspect element for font sizing
- **Layout**: Measure spacing with browser tools

---

**Last Updated**: October 16, 2025
**Maintained By**: Automation Agent
**Design Version**: 2.0 (MIT Sloan Blue Theme)
