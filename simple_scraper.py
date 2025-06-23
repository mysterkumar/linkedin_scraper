#!/usr/bin/env python3
"""
Simple LinkedIn Profile Scraper with Excel Export
Easier to use version of the enhanced scraper
"""

import os
import sys
import json
import time
import random
from datetime import datetime
from typing import List, Optional
import pandas as pd
from dataclasses import asdict

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    
    from linkedin_scraper import Person, actions
    print("LinkedIn scraper modules imported successfully!")
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)


class SimpleLinkedInScraper:
    """Simple LinkedIn scraper with basic functionality"""
    
    def __init__(self):
        self.driver = None
        self.scraped_data = []
        self.scraped_urls = set()
    
    def setup_driver(self, headless=False):
        """Setup Chrome WebDriver"""
        try:
            chrome_options = Options()
            
            if headless:
                chrome_options.add_argument("--headless")
            
            # Basic options for stability
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Use webdriver-manager to handle ChromeDriver
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            except Exception:
                # Fallback to default Chrome driver
                self.driver = webdriver.Chrome(options=chrome_options)
            
            print("✓ ChromeDriver initialized successfully")
            return True
            
        except Exception as e:
            print(f"✗ Failed to setup ChromeDriver: {e}")
            print("Make sure Chrome browser is installed and accessible")
            return False
    
    def login(self, email=None, password=None):
        """Login to LinkedIn"""
        if not self.driver:
            if not self.setup_driver():
                return False
        
        try:
            print("Logging into LinkedIn...")
            actions.login(self.driver, email, password)
            print("✓ Successfully logged into LinkedIn")
            return True
            
        except Exception as e:
            print(f"✗ Failed to login: {e}")
            return False
    
    def scrape_single_profile(self, linkedin_url):
        """Scrape a single LinkedIn profile"""
        if linkedin_url in self.scraped_urls:
            print(f"Profile already scraped: {linkedin_url}")
            return None
        
        try:
            print(f"Scraping: {linkedin_url}")
            
            # Add random delay
            time.sleep(random.uniform(2, 4))
            
            # Scrape the profile
            person = Person(
                linkedin_url=linkedin_url,
                driver=self.driver,
                scrape=True,
                close_on_complete=False
            )
            
            if person.name:
                # Convert to dictionary for easier handling
                profile_data = {
                    'scraped_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'name': person.name,
                    'linkedin_url': person.linkedin_url,
                    'company': person.company,
                    'job_title': person.job_title,
                    'about': ' '.join(person.about) if person.about else '',
                    'location': getattr(person, 'location', ''),
                    'experiences_count': len(person.experiences) if person.experiences else 0,
                    'educations_count': len(person.educations) if person.educations else 0,
                    'connections_count': len(person.contacts) if person.contacts else 0
                }
                
                # Add top experiences
                if person.experiences:
                    for i, exp in enumerate(person.experiences[:3]):  # Top 3 experiences
                        profile_data[f'experience_{i+1}_title'] = exp.position_title or ''
                        profile_data[f'experience_{i+1}_company'] = exp.institution_name or ''
                        profile_data[f'experience_{i+1}_duration'] = exp.duration or ''
                        profile_data[f'experience_{i+1}_location'] = exp.location or ''
                
                # Add education
                if person.educations:
                    for i, edu in enumerate(person.educations[:2]):  # Top 2 educations
                        profile_data[f'education_{i+1}_institution'] = edu.institution_name or ''
                        profile_data[f'education_{i+1}_degree'] = edu.degree or ''
                
                self.scraped_data.append(profile_data)
                self.scraped_urls.add(linkedin_url)
                
                print(f"✓ Successfully scraped: {person.name}")
                return profile_data
            else:
                print(f"✗ No data found for: {linkedin_url}")
                return None
                
        except Exception as e:
            print(f"✗ Failed to scrape {linkedin_url}: {e}")
            return None
    
    def scrape_multiple_profiles(self, profile_urls):
        """Scrape multiple LinkedIn profiles"""
        print(f"Starting to scrape {len(profile_urls)} profiles...")
        
        success_count = 0
        
        for i, url in enumerate(profile_urls, 1):
            print(f"\\n[{i}/{len(profile_urls)}] ", end="")
            
            result = self.scrape_single_profile(url)
            if result:
                success_count += 1
            
            # Save data every 5 profiles
            if i % 5 == 0:
                self.save_to_excel()
                print(f"Intermediate save completed ({success_count} profiles scraped so far)")
        
        print(f"\\n=== Scraping Complete ===")
        print(f"Successfully scraped: {success_count}/{len(profile_urls)} profiles")
        
        return success_count
    
    def save_to_excel(self, filename=None):
        """Save scraped data to Excel file"""
        if not self.scraped_data:
            print("No data to save")
            return None
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"linkedin_profiles_{timestamp}.xlsx"
        
        try:
            df = pd.DataFrame(self.scraped_data)
            df.to_excel(filename, index=False, engine='openpyxl')
            print(f"✓ Data saved to: {filename}")
            return filename
            
        except Exception as e:
            print(f"✗ Failed to save Excel file: {e}")
            return None
    
    def save_to_json(self, filename=None):
        """Save scraped data to JSON file"""
        if not self.scraped_data:
            print("No data to save")
            return None
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"linkedin_profiles_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
            print(f"✓ Data saved to: {filename}")
            return filename
            
        except Exception as e:
            print(f"✗ Failed to save JSON file: {e}")
            return None
    
    def cleanup(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("✓ Browser closed")


def main():
    """Main function for interactive usage"""
    
    print("=== Simple LinkedIn Profile Scraper ===\\n")
    
    # Sample profile URLs - replace with your target profiles
    sample_profiles = [
        "https://www.linkedin.com/in/satyanadella/",
        "https://www.linkedin.com/in/sundarpichai/",
        "https://www.linkedin.com/in/jeffweiner08/",
        "https://www.linkedin.com/in/sherylsandberg/",
        "https://www.linkedin.com/in/reidhoffman/"
    ]
    
    scraper = SimpleLinkedInScraper()
    
    try:
        # Login to LinkedIn
        print("Please log in to LinkedIn...")
        if not scraper.login():
            print("Failed to login. Exiting.")
            return
        
        print("\\nChoose an option:")
        print("1. Scrape sample profiles (5 profiles)")
        print("2. Enter custom profile URLs")
        print("3. Load URLs from file")
        
        choice = input("\\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            profile_urls = sample_profiles
            
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
                    print("Invalid LinkedIn profile URL. Please try again.")
            
        elif choice == "3":
            filename = input("Enter filename containing URLs (one per line): ").strip()
            try:
                with open(filename, 'r') as f:
                    profile_urls = [line.strip() for line in f if line.strip() and "linkedin.com/in/" in line]
            except FileNotFoundError:
                print(f"File not found: {filename}")
                return
            except Exception as e:
                print(f"Error reading file: {e}")
                return
        
        else:
            print("Invalid choice. Exiting.")
            return
        
        if not profile_urls:
            print("No valid profile URLs found. Exiting.")
            return
        
        print(f"\\nFound {len(profile_urls)} profile URLs to scrape.")
        confirm = input("Continue? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("Cancelled.")
            return
        
        # Start scraping
        success_count = scraper.scrape_multiple_profiles(profile_urls)
        
        # Save final results
        if success_count > 0:
            excel_file = scraper.save_to_excel()
            json_file = scraper.save_to_json()
            
            print(f"\\n=== Results ===")
            print(f"Profiles scraped: {success_count}")
            if excel_file:
                print(f"Excel file: {excel_file}")
            if json_file:
                print(f"JSON file: {json_file}")
        else:
            print("No profiles were successfully scraped.")
    
    except KeyboardInterrupt:
        print("\\nScraping interrupted by user.")
    
    except Exception as e:
        print(f"\\nError: {e}")
    
    finally:
        scraper.cleanup()


if __name__ == "__main__":
    main()
