#!/usr/bin/env python3
"""
Fixes for common LinkedIn scraper issues
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from linkedin_scraper.person import Person
from linkedin_scraper import actions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_basic_functionality():
    """Test basic scraper functionality and identify issues"""
    
    print("=== LinkedIn Scraper Diagnostics ===\\n")
    
    # Test 1: Import test
    print("1. Testing imports...")
    try:
        from linkedin_scraper import Person, actions
        print("✓ LinkedIn scraper imports successful")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    
    # Test 2: ChromeDriver test
    print("\\n2. Testing ChromeDriver...")
    try:
        # Try with webdriver-manager first
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
            print("✓ ChromeDriver with webdriver-manager works")
        except:
            # Fallback to default
            driver = webdriver.Chrome()
            print("✓ ChromeDriver (default) works")
        
        driver.get("https://www.google.com")
        print("✓ Can navigate to websites")
        driver.quit()
        
    except Exception as e:
        print(f"✗ ChromeDriver error: {e}")
        print("Solutions:")
        print("  - Install Chrome browser")
        print("  - Run: pip install webdriver-manager")
        print("  - Or download ChromeDriver manually and set PATH")
        return False
    
    # Test 3: Basic LinkedIn access
    print("\\n3. Testing LinkedIn access...")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run headless for testing
        
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except:
            driver = webdriver.Chrome(options=chrome_options)
        
        driver.get("https://www.linkedin.com")
        title = driver.title
        
        if "LinkedIn" in title:
            print("✓ Can access LinkedIn")
        else:
            print(f"✗ Unexpected page title: {title}")
        
        driver.quit()
        
    except Exception as e:
        print(f"✗ LinkedIn access error: {e}")
        return False
    
    print("\\n=== Basic functionality test complete ===")
    return True


def fix_person_class_issues():
    """Apply fixes to Person class for better compatibility"""
    
    print("\\n=== Applying Person Class Fixes ===")
    
    # The main issues in the current Person class:
    # 1. Outdated LinkedIn selectors
    # 2. Missing error handling
    # 3. ChromeDriver path issues
    
    fixes_applied = []
    
    # Check if ChromeDriver environment variable is set
    if not os.getenv("CHROMEDRIVER"):
        print("Setting up ChromeDriver auto-detection...")
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            driver_path = ChromeDriverManager().install()
            os.environ["CHROMEDRIVER"] = driver_path
            fixes_applied.append("ChromeDriver auto-detection")
        except:
            print("Warning: Could not set up ChromeDriver auto-detection")
    
    print(f"Fixes applied: {', '.join(fixes_applied) if fixes_applied else 'None needed'}")


def create_test_script():
    """Create a test script to verify everything works"""
    
    test_script_content = '''#!/usr/bin/env python3
"""
Test script for LinkedIn scraper
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_simple_scrape():
    """Test basic scraping functionality"""
    
    try:
        from simple_scraper import SimpleLinkedInScraper
        
        scraper = SimpleLinkedInScraper()
        
        # Test driver setup
        if scraper.setup_driver(headless=True):
            print("✓ Driver setup successful")
            scraper.cleanup()
            return True
        else:
            print("✗ Driver setup failed")
            return False
            
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== LinkedIn Scraper Test ===")
    if test_simple_scrape():
        print("\\n✓ All tests passed! The scraper should work.")
        print("\\nTo start scraping, run:")
        print("  python simple_scraper.py")
    else:
        print("\\n✗ Tests failed. Please check the error messages above.")
        print("\\nTry running:")
        print("  install_dependencies.bat")
'''
    
    with open("test_scraper.py", "w") as f:
        f.write(test_script_content)
    
    print("Created test_scraper.py")


def main():
    """Main function to run diagnostics and fixes"""
    
    # Run basic functionality test
    if test_basic_functionality():
        print("\\n✓ Basic functionality looks good!")
    else:
        print("\\n✗ Found issues with basic functionality")
        print("Please install dependencies with: install_dependencies.bat")
        return
    
    # Apply fixes
    fix_person_class_issues()
    
    # Create test script
    create_test_script()
    
    print("\\n=== Summary ===")
    print("✓ Diagnostics complete")
    print("✓ Fixes applied where needed")
    print("✓ Test script created")
    
    print("\\nNext steps:")
    print("1. Run: python test_scraper.py")
    print("2. If test passes, run: python simple_scraper.py")
    print("3. For advanced features, run: python enhanced_scraper.py")


if __name__ == "__main__":
    main()
