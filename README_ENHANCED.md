# Enhanced LinkedIn Scraper System

A comprehensive LinkedIn profile scraper with random profile discovery, duplicate prevention, and Excel export capabilities.

## Features

✅ **Smart Profile Discovery**

- Discover profiles from company employee pages
- Find profiles through "People Also Viewed" sections
- Search-based profile discovery
- Random profile injection to avoid patterns

✅ **Duplicate Prevention**

- Automatic tracking of scraped profiles
- JSON database to prevent re-scraping
- URL normalization for consistent comparison

✅ **Excel Export**

- Comprehensive profile data export
- Multiple file formats (Excel, JSON)
- Periodic saves during scraping

✅ **Enhanced Reliability**

- Automatic ChromeDriver management
- Retry logic for failed requests
- Rate limiting and random delays
- Stealth browsing options

## Quick Start

### 1. Install Dependencies

Run the batch file to install all required packages:

```bash
install_dependencies.bat
```

Or manually install:

```bash
pip install -r requirements.txt
```

### 2. Test Installation

```bash
python fix_issues.py
python test_scraper.py
```

### 3. Run Simple Scraper

For basic usage:

```bash
python simple_scraper.py
```

### 4. Run Enhanced Scraper

For advanced features:

```bash
python enhanced_scraper.py
```

## Usage Options

### Option 1: Simple Scraper (Recommended for beginners)

The `simple_scraper.py` provides an easy-to-use interface:

1. **Interactive Mode**: Run the script and follow prompts
2. **Sample Profiles**: Uses built-in sample LinkedIn profiles
3. **Custom URLs**: Enter your own profile URLs
4. **File Input**: Load URLs from a text file

Example:

```python
from simple_scraper import SimpleLinkedInScraper

scraper = SimpleLinkedInScraper()
scraper.login()  # Will prompt for LinkedIn credentials

# Scrape specific profiles
profiles = [
    "https://www.linkedin.com/in/satyanadella/",
    "https://www.linkedin.com/in/sundarpichai/"
]

scraper.scrape_multiple_profiles(profiles)
scraper.save_to_excel("my_profiles.xlsx")
scraper.cleanup()
```

### Option 2: Enhanced Scraper (Advanced features)

The `enhanced_scraper.py` provides advanced discovery and management:

```python
from enhanced_scraper import EnhancedLinkedInScraper

scraper = EnhancedLinkedInScraper(headless=False)
scraper.login()

# Automatic profile discovery and scraping
scraper.discover_and_scrape(
    seed_profiles=[
        "https://www.linkedin.com/in/satyanadella/",
        "https://www.linkedin.com/in/sundarpichai/"
    ],
    company_urls=[
        "https://www.linkedin.com/company/microsoft/",
        "https://www.linkedin.com/company/google/"
    ],
    search_terms=["Software Engineer", "Data Scientist"],
    max_profiles=50
)

scraper.cleanup()
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
LINKEDIN_EMAIL=your-email@example.com
LINKEDIN_PASSWORD=your-password
MAX_PROFILES=50
HEADLESS_MODE=False
```

### Profile Discovery Sources

1. **Seed Profiles**: Existing LinkedIn profiles to discover connections from
2. **Company URLs**: Company pages to find employee profiles
3. **Search Terms**: Keywords to search for relevant profiles

## Output Files

### Excel Export (`linkedin_profiles_YYYYMMDD_HHMMSS.xlsx`)

Contains columns:

- Basic info: Name, LinkedIn URL, Company, Job Title
- Contact info: Location, About section
- Experience: Position titles, companies, durations
- Education: Institutions, degrees
- Statistics: Connection counts, experience counts

### JSON Database (`scraped_profiles.json`)

Stores complete profile data including:

- Full experience history
- Complete education records
- All contact information
- Interests and accomplishments
- Scraping metadata

## Anti-Detection Features

1. **Random Delays**: Variable delays between requests
2. **User Agent Rotation**: Different browser signatures
3. **Stealth Options**: Disabled automation indicators
4. **Rate Limiting**: Respects LinkedIn's rate limits
5. **Error Handling**: Graceful handling of blocks/captchas

## Troubleshooting

### Common Issues

1. **ChromeDriver not found**

   - Solution: The scraper automatically downloads ChromeDriver
   - Alternative: Download manually and set CHROMEDRIVER environment variable

2. **Login fails**

   - Check credentials
   - LinkedIn may require 2FA - handle manually in browser
   - Account may be temporarily restricted

3. **No data scraped**

   - LinkedIn may be blocking the request
   - Try running with `headless=False` to see what's happening
   - Add longer delays between requests

4. **Import errors**
   - Run `install_dependencies.bat`
   - Check Python version (3.7+ required)

### Debug Mode

Run with debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Rate Limiting & Ethics

⚠️ **Important Guidelines**:

1. **Respect LinkedIn's Terms**: This tool is for educational/research purposes
2. **Rate Limiting**: Don't scrape too aggressively (max 20-30 profiles/hour recommended)
3. **Public Data Only**: Only scrapes publicly visible information
4. **User Consent**: Ensure you have permission to scrape specific profiles
5. **Data Protection**: Handle scraped data responsibly per GDPR/privacy laws

## File Structure

```
linkedin_scraper/
├── linkedin_scraper/          # Original scraper package
│   ├── __init__.py
│   ├── person.py
│   ├── actions.py
│   └── ...
├── simple_scraper.py          # Easy-to-use scraper
├── enhanced_scraper.py        # Advanced scraper with discovery
├── fix_issues.py              # Diagnostic and fix script
├── test_scraper.py            # Test functionality
├── install_dependencies.bat   # Windows dependency installer
├── requirements.txt           # Python dependencies
├── .env.example              # Configuration template
└── README.md                 # This file
```

## Examples

### Example 1: Scrape Tech CEOs

```python
from simple_scraper import SimpleLinkedInScraper

tech_ceos = [
    "https://www.linkedin.com/in/satyanadella/",      # Microsoft
    "https://www.linkedin.com/in/sundarpichai/",      # Google
    "https://www.linkedin.com/in/jeffweiner08/",      # LinkedIn
    "https://www.linkedin.com/in/sherylsandberg/",    # Meta
]

scraper = SimpleLinkedInScraper()
scraper.login()
scraper.scrape_multiple_profiles(tech_ceos)
scraper.save_to_excel("tech_ceos.xlsx")
scraper.cleanup()
```

### Example 2: Company Employee Discovery

```python
from enhanced_scraper import EnhancedLinkedInScraper

scraper = EnhancedLinkedInScraper()
scraper.login()

scraper.discover_and_scrape(
    company_urls=[
        "https://www.linkedin.com/company/microsoft/",
        "https://www.linkedin.com/company/google/"
    ],
    max_profiles=20
)

scraper.cleanup()
```

### Example 3: Search-based Discovery

```python
scraper.discover_and_scrape(
    search_terms=[
        "Machine Learning Engineer",
        "Data Scientist",
        "Product Manager"
    ],
    max_profiles=30
)
```

## License

This project is for educational and research purposes. Please respect LinkedIn's Terms of Service and use responsibly.

## Support

If you encounter issues:

1. Run `python fix_issues.py` for diagnostics
2. Check the troubleshooting section above
3. Ensure all dependencies are installed correctly
4. Verify LinkedIn credentials and account status

---

**Happy Scraping! 🚀**
