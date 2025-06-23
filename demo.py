#!/usr/bin/env python3
"""
Quick Demo - LinkedIn Scraper
A simple demonstration of the working scraper
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_basic_scraping():
    """Demonstrate basic scraping functionality"""
    
    print("=== LinkedIn Scraper Demo ===\\n")
    
    # Test imports first
    print("Testing imports...")
    try:
        from working_scraper import WorkingLinkedInScraper
        print("✓ Scraper imports successful")
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        print("Please run: install_dependencies.bat")
        return False
    
    # Create scraper instance
    print("\\nInitializing scraper...")
    scraper = WorkingLinkedInScraper(headless=True)  # Use headless for demo
    
    try:
        # Test driver setup
        print("Setting up ChromeDriver...")
        if scraper.setup_driver():
            print("✓ ChromeDriver ready")
        else:
            print("✗ ChromeDriver setup failed")
            return False
        
        # Test LinkedIn access
        print("Testing LinkedIn access...")
        scraper.driver.get("https://www.linkedin.com")
        title = scraper.driver.title
        
        if "LinkedIn" in title:
            print("✓ Can access LinkedIn")
        else:
            print(f"✗ Unexpected page: {title}")
        
        print("\\n=== Demo Complete ===")
        print("The scraper is ready to use!")
        print("\\nTo start scraping:")
        print("1. Run: python working_scraper.py")
        print("2. Login when prompted")
        print("3. Choose profiles to scrape")
        print("4. Data will be saved to Excel file")
        
        return True
        
    except Exception as e:
        print(f"✗ Demo failed: {e}")
        return False
        
    finally:
        scraper.cleanup()

def show_sample_usage():
    """Show sample usage code"""
    
    print("\\n=== Sample Usage Code ===\\n")
    
    sample_code = '''
# Example 1: Basic usage
from working_scraper import WorkingLinkedInScraper

scraper = WorkingLinkedInScraper()
scraper.login_to_linkedin()  # Will prompt for credentials

# Sample profiles to scrape
profiles = [
    "https://www.linkedin.com/in/satyanadella/",
    "https://www.linkedin.com/in/sundarpichai/",
    "https://www.linkedin.com/in/jeffweiner08/"
]

# Scrape profiles
scraper.scrape_multiple_profiles(profiles)

# Save to Excel
scraper.save_to_excel("tech_leaders.xlsx")
scraper.cleanup()

# ===================================

# Example 2: Advanced usage with enhanced scraper
from enhanced_scraper import EnhancedLinkedInScraper

scraper = EnhancedLinkedInScraper()
scraper.login()

# Automatic profile discovery and scraping
scraper.discover_and_scrape(
    company_urls=[
        "https://www.linkedin.com/company/microsoft/",
        "https://www.linkedin.com/company/google/"
    ],
    search_terms=["Software Engineer", "Data Scientist"],
    max_profiles=20
)

scraper.cleanup()
'''
    
    print(sample_code)

def show_file_structure():
    """Show the current file structure"""
    
    print("\\n=== File Structure ===\\n")
    
    files = {
        "🚀 Main Scripts": [
            "working_scraper.py - Complete working scraper (RECOMMENDED)",
            "simple_scraper.py - Simple interface version", 
            "enhanced_scraper.py - Advanced features with profile discovery"
        ],
        "🔧 Setup & Utilities": [
            "install_dependencies.bat - Install all required packages",
            "fix_issues.py - Diagnostic and fix script",
            "SOLUTION_SUMMARY.py - Shows all improvements made",
            "demo.py - This demonstration script"
        ],
        "📚 Documentation": [
            "README_ENHANCED.md - Complete documentation",
            ".env.example - Configuration template",
            "requirements.txt - Updated dependencies"
        ],
        "📁 Original Files": [
            "linkedin_scraper/ - Original scraper package (enhanced)",
            "samples/ - Original sample scripts",
            "test/ - Original test scripts"
        ]
    }
    
    for category, file_list in files.items():
        print(f"{category}")
        for file_desc in file_list:
            print(f"  {file_desc}")
        print()

def main():
    """Main demo function"""
    
    print("LinkedIn Scraper - Quick Demo & Instructions\\n")
    print("=" * 50)
    
    # Run basic demo
    demo_success = demo_basic_scraping()
    
    print("\\n" + "=" * 50)
    
    # Show usage examples
    show_sample_usage()
    
    print("=" * 50)
    
    # Show file structure
    show_file_structure()
    
    print("=" * 50)
    
    print("\\n🎯 NEXT STEPS:")
    
    if demo_success:
        print("✓ Demo successful! You're ready to start scraping.")
        print("\\n1. Run the main scraper:")
        print("   python working_scraper.py")
        print("\\n2. For advanced features:")
        print("   python enhanced_scraper.py")
    else:
        print("✗ Demo had issues. Try these steps:")
        print("\\n1. Install dependencies:")
        print("   install_dependencies.bat")
        print("\\n2. Run diagnostics:")
        print("   python fix_issues.py")
        print("\\n3. Try demo again:")
        print("   python demo.py")
    
    print("\\n📖 For detailed instructions:")
    print("   See README_ENHANCED.md")
    
    print("\\n⚠️  Remember:")
    print("- Respect LinkedIn's Terms of Service")
    print("- Use reasonable delays between requests")
    print("- Handle personal data responsibly")

if __name__ == "__main__":
    main()
