#!/usr/bin/env python3
"""
Complete LinkedIn Scraper Solution
Addresses all current issues and provides working functionality
"""

import os
import sys
import json
import time
import random
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Try to import required packages, provide helpful error messages
try:
    import pandas as pd
    logger.info("✓ pandas imported")
except ImportError:
    logger.error("✗ pandas not found. Run: pip install pandas")
    sys.exit(1)

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    logger.info("✓ selenium imported")
except ImportError:
    logger.error("✗ selenium not found. Run: pip install selenium")
    sys.exit(1)

try:
    from webdriver_manager.chrome import ChromeDriverManager
    logger.info("✓ webdriver-manager imported")
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    logger.warning("webdriver-manager not found. Will try default ChromeDriver")
    USE_WEBDRIVER_MANAGER = False

# Add current directory to path for local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to import original LinkedIn scraper modules
try:
    from linkedin_scraper import Person, actions
    logger.info("✓ linkedin_scraper imported")
    USE_ORIGINAL_SCRAPER = True
except ImportError:
    logger.warning("Original linkedin_scraper not available. Using built-in methods")
    USE_ORIGINAL_SCRAPER = False


class WorkingLinkedInScraper:
    """
    A working LinkedIn scraper that addresses common issues
    """
    
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        self.scraped_profiles = []
        self.scraped_urls = set()
        
    def setup_driver(self):
        """Setup Chrome WebDriver with fallback options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Add stability options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            if USE_WEBDRIVER_MANAGER:
                # Try webdriver-manager first
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("✓ ChromeDriver setup with webdriver-manager")
            else:
                # Fallback to default ChromeDriver
                self.driver = webdriver.Chrome(options=chrome_options)
                logger.info("✓ ChromeDriver setup with default driver")
            
            # Remove webdriver property for stealth
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup ChromeDriver: {e}")
            logger.error("Solutions:")
            logger.error("1. Install Chrome browser")
            logger.error("2. Run: pip install webdriver-manager")
            logger.error("3. Download ChromeDriver manually and add to PATH")
            return False
    
    def login_to_linkedin(self, email=None, password=None):
        """Login to LinkedIn with enhanced error handling"""
        if not self.driver:
            if not self.setup_driver():
                return False
        
        try:
            if USE_ORIGINAL_SCRAPER:
                # Use original actions module if available
                actions.login(self.driver, email, password)
                logger.info("✓ Logged in using original scraper")
            else:
                # Manual login process
                self._manual_login(email, password)
                logger.info("✓ Logged in using manual process")
            
            return True
            
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
    
    def _manual_login(self, email=None, password=None):
        """Manual LinkedIn login process"""
        if not email:
            email = input("LinkedIn Email: ")
        if not password:
            import getpass
            password = getpass.getpass("LinkedIn Password: ")
        
        self.driver.get("https://www.linkedin.com/login")
        
        # Wait for login page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        
        # Enter credentials
        email_field = self.driver.find_element(By.ID, "username")
        password_field = self.driver.find_element(By.ID, "password")
        
        email_field.send_keys(email)
        password_field.send_keys(password)
        password_field.submit()
        
        # Wait for successful login
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "global-nav__primary-link"))
        )
    
    def scrape_profile_basic(self, linkedin_url):
        """Basic profile scraping with error handling"""
        if linkedin_url in self.scraped_urls:
            logger.info(f"Profile already scraped: {linkedin_url}")
            return None
        
        try:
            logger.info(f"Scraping: {linkedin_url}")
            
            # Add random delay
            time.sleep(random.uniform(2, 5))
            
            if USE_ORIGINAL_SCRAPER:
                # Use original Person class if available
                person = Person(
                    linkedin_url=linkedin_url,
                    driver=self.driver,
                    scrape=True,
                    close_on_complete=False
                )
                
                if person.name:
                    profile_data = self._convert_person_to_dict(person)
                    self.scraped_profiles.append(profile_data)
                    self.scraped_urls.add(linkedin_url)
                    logger.info(f"✓ Scraped: {person.name}")
                    return profile_data
            else:
                # Manual scraping
                profile_data = self._manual_scrape_profile(linkedin_url)
                if profile_data:
                    self.scraped_profiles.append(profile_data)
                    self.scraped_urls.add(linkedin_url)
                    logger.info(f"✓ Scraped: {profile_data['name']}")
                    return profile_data
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to scrape {linkedin_url}: {e}")
            return None
    
    def _convert_person_to_dict(self, person):
        """Convert Person object to dictionary"""
        return {
            'name': person.name,
            'linkedin_url': person.linkedin_url,
            'about': ' '.join(person.about) if person.about else '',
            'company': person.company,
            'job_title': person.job_title,
            'experiences_count': len(person.experiences) if person.experiences else 0,
            'educations_count': len(person.educations) if person.educations else 0,
            'scraped_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _manual_scrape_profile(self, linkedin_url):
        """Manual profile scraping without original Person class"""
        try:
            self.driver.get(linkedin_url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "main"))
            )
            
            profile_data = {
                'name': '',
                'linkedin_url': linkedin_url,
                'about': '',
                'company': '',
                'job_title': '',
                'location': '',
                'scraped_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Try to get name
            try:
                name_elem = self.driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge")
                profile_data['name'] = name_elem.text.strip()
            except NoSuchElementException:
                try:
                    name_elem = self.driver.find_element(By.CSS_SELECTOR, ".pv-text-details__left-panel h1")
                    profile_data['name'] = name_elem.text.strip()
                except NoSuchElementException:
                    logger.warning(f"Could not find name for {linkedin_url}")
            
            # Try to get current position
            try:
                position_elem = self.driver.find_element(By.CSS_SELECTOR, ".text-body-medium.break-words")
                profile_data['job_title'] = position_elem.text.strip()
            except NoSuchElementException:
                pass
            
            # Try to get location
            try:
                location_elem = self.driver.find_element(By.CSS_SELECTOR, ".text-body-small.inline.t-black--light.break-words")
                profile_data['location'] = location_elem.text.strip()
            except NoSuchElementException:
                pass
            
            return profile_data if profile_data['name'] else None
            
        except Exception as e:
            logger.error(f"Manual scraping failed for {linkedin_url}: {e}")
            return None
    
    def scrape_multiple_profiles(self, profile_urls, max_profiles=None):
        """Scrape multiple profiles with progress tracking"""
        if max_profiles:
            profile_urls = profile_urls[:max_profiles]
        
        logger.info(f"Starting to scrape {len(profile_urls)} profiles")
        
        success_count = 0
        for i, url in enumerate(profile_urls, 1):
            logger.info(f"[{i}/{len(profile_urls)}] Processing: {url}")
            
            result = self.scrape_profile_basic(url)
            if result:
                success_count += 1
                
                # Save progress every 5 profiles
                if success_count % 5 == 0:
                    self.save_to_excel()
                    logger.info(f"Progress saved: {success_count} profiles completed")
        
        logger.info(f"Scraping complete: {success_count}/{len(profile_urls)} profiles successful")
        return success_count
    
    def save_to_excel(self, filename=None):
        """Save scraped data to Excel file"""
        if not self.scraped_profiles:
            logger.warning("No data to save")
            return None
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"linkedin_profiles_{timestamp}.xlsx"
        
        try:
            df = pd.DataFrame(self.scraped_profiles)
            df.to_excel(filename, index=False, engine='openpyxl')
            logger.info(f"✓ Data saved to: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Failed to save Excel: {e}")
            return None
    
    def save_to_json(self, filename=None):
        """Save scraped data to JSON file"""
        if not self.scraped_profiles:
            logger.warning("No data to save")
            return None
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"linkedin_profiles_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.scraped_profiles, f, indent=2, ensure_ascii=False)
            logger.info(f"✓ Data saved to: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Failed to save JSON: {e}")
            return None
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            logger.info("✓ Browser closed")


def get_sample_profiles():
    """Get sample LinkedIn profiles for testing"""
    return [
        "https://www.linkedin.com/in/satyanadella/",
        "https://www.linkedin.com/in/sundarpichai/",
        "https://www.linkedin.com/in/jeffweiner08/",
        "https://www.linkedin.com/in/sherylsandberg/",
        "https://www.linkedin.com/in/reidhoffman/"
    ]


def main():
    """Main function with interactive interface"""
    print("=== Working LinkedIn Profile Scraper ===\\n")
    
    scraper = WorkingLinkedInScraper(headless=False)
    
    try:
        # Setup and login
        logger.info("Setting up scraper...")
        if not scraper.login_to_linkedin():
            logger.error("Failed to login. Exiting.")
            return
        
        # Get profiles to scrape
        print("\\nChoose profiles to scrape:")
        print("1. Sample profiles (5 tech leaders)")
        print("2. Enter custom URLs")
        print("3. Load from file")
        
        choice = input("\\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            profile_urls = get_sample_profiles()
            print(f"Using {len(profile_urls)} sample profiles")
            
        elif choice == "2":
            print("\\nEnter LinkedIn profile URLs (one per line, empty line to finish):")
            profile_urls = []
            while True:
                url = input().strip()
                if not url:
                    break
                if "linkedin.com/in/" in url:
                    profile_urls.append(url)
                else:
                    print("Invalid LinkedIn URL. Try again.")
                    
        elif choice == "3":
            filename = input("Enter filename with URLs: ").strip()
            try:
                with open(filename, 'r') as f:
                    profile_urls = [line.strip() for line in f if line.strip() and "linkedin.com/in/" in line]
                print(f"Loaded {len(profile_urls)} URLs from file")
            except FileNotFoundError:
                print(f"File not found: {filename}")
                return
                
        else:
            print("Invalid choice")
            return
        
        if not profile_urls:
            print("No valid URLs found")
            return
        
        # Confirm and start scraping
        print(f"\\nReady to scrape {len(profile_urls)} profiles")
        if input("Continue? (y/n): ").lower() != 'y':
            print("Cancelled")
            return
        
        # Start scraping
        success_count = scraper.scrape_multiple_profiles(profile_urls)
        
        # Save results
        if success_count > 0:
            excel_file = scraper.save_to_excel()
            json_file = scraper.save_to_json()
            
            print(f"\\n=== Results ===")
            print(f"Profiles scraped: {success_count}")
            print(f"Excel file: {excel_file}")
            print(f"JSON file: {json_file}")
        else:
            print("No profiles were successfully scraped")
    
    except KeyboardInterrupt:
        print("\\nScraping interrupted")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        scraper.cleanup()


if __name__ == "__main__":
    main()
