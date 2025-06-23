#!/usr/bin/env python3
"""
Test script to verify all scraper components are working
"""

def test_imports():
    """Test all critical imports"""
    
    print("Testing imports...")
    
    try:
        # Test basic dependencies
        import selenium
        print("✓ Selenium")
        
        import pandas
        print("✓ Pandas")
        
        import openpyxl
        print("✓ OpenPyXL")
        
        from webdriver_manager.chrome import ChromeDriverManager
        print("✓ WebDriver Manager")
        
        # Test fake_useragent with fallback
        try:
            from fake_useragent import UserAgent
            ua = UserAgent()
            print("✓ Fake UserAgent")
        except ImportError:
            print("⚠ Fake UserAgent not available (using fallback)")
        
        # Test our scrapers
        from linkedin_scraper import Person, actions
        print("✓ LinkedIn Scraper Core")
        
        import simple_scraper
        print("✓ Simple Scraper")
        
        import enhanced_scraper
        print("✓ Enhanced Scraper")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_webdriver():
    """Test WebDriver setup"""
    
    print("\nTesting WebDriver setup...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Create driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Test navigation
        driver.get("https://www.google.com")
        title = driver.title
        
        driver.quit()
        
        if "Google" in title:
            print("✓ WebDriver working correctly")
            return True
        else:
            print(f"✗ Unexpected page title: {title}")
            return False
            
    except Exception as e:
        print(f"✗ WebDriver error: {e}")
        return False

def main():
    """Main test function"""
    
    print("=== LinkedIn Scraper - System Test ===\n")
    
    # Test imports
    imports_ok = test_imports()
    
    # Test WebDriver
    webdriver_ok = test_webdriver()
    
    print("\n" + "="*50)
    print("TEST RESULTS:")
    print(f"Imports: {'✓ PASS' if imports_ok else '✗ FAIL'}")
    print(f"WebDriver: {'✓ PASS' if webdriver_ok else '✗ FAIL'}")
    
    if imports_ok and webdriver_ok:
        print("\n🎉 ALL TESTS PASSED!")
        print("\nYou can now run:")
        print("  python simple_scraper.py")
        print("  python enhanced_scraper.py")
    else:
        print("\n⚠ SOME TESTS FAILED")
        print("\nTry running:")
        print("  install_dependencies.bat")
        print("  pip install -r requirements.txt")

if __name__ == "__main__":
    main()
