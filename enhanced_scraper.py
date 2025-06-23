#!/usr/bin/env python3
"""
Enhanced LinkedIn Scraper with Random Profile Discovery and Excel Export
"""

import os
import json
import time
import random
import hashlib
from datetime import datetime
from typing import List, Dict, Set, Optional
from urllib.parse import urljoin, urlparse
import pandas as pd
from dataclasses import asdict
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, WebDriverException,
    StaleElementReferenceException
)
from webdriver_manager.chrome import ChromeDriverManager

# Handle fake_useragent import with fallback
try:
    from fake_useragent import UserAgent
    HAS_FAKE_USERAGENT = True
except ImportError:
    HAS_FAKE_USERAGENT = False
    class UserAgent:
        @property
        def random(self):
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

from linkedin_scraper import Person, actions
from linkedin_scraper.objects import Experience, Education, Contact

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linkedin_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ProfileDatabase:
    """Manages scraped profiles and prevents duplicates"""
    
    def __init__(self, db_file: str = "scraped_profiles.json"):
        self.db_file = db_file
        self.profiles: Dict[str, Dict] = self._load_database()
        self.scraped_urls: Set[str] = set(self.profiles.keys())
    
    def _load_database(self) -> Dict[str, Dict]:
        """Load existing profile database"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load database: {e}")
                return {}
        return {}
    
    def save_database(self):
        """Save profile database to file"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.profiles, f, indent=2, ensure_ascii=False, default=str)
            logger.info(f"Database saved with {len(self.profiles)} profiles")
        except Exception as e:
            logger.error(f"Failed to save database: {e}")
    
    def is_scraped(self, linkedin_url: str) -> bool:
        """Check if a profile URL has already been scraped"""
        normalized_url = self._normalize_url(linkedin_url)
        return normalized_url in self.scraped_urls
    
    def add_profile(self, person: Person):
        """Add a scraped profile to the database"""
        try:
            normalized_url = self._normalize_url(person.linkedin_url)
            
            # Convert person object to dictionary
            profile_data = {
                'scraped_at': datetime.now().isoformat(),
                'name': person.name,
                'about': person.about,
                'linkedin_url': person.linkedin_url,
                'company': person.company,
                'job_title': person.job_title,
                'experiences': [asdict(exp) for exp in person.experiences] if person.experiences else [],
                'educations': [asdict(edu) for edu in person.educations] if person.educations else [],
                'contacts': [asdict(contact) for contact in person.contacts] if person.contacts else [],
                'interests': [getattr(interest, 'title', str(interest)) for interest in person.interests] if person.interests else [],
                'accomplishments': [asdict(acc) for acc in person.accomplishments] if person.accomplishments else []
            }
            
            self.profiles[normalized_url] = profile_data
            self.scraped_urls.add(normalized_url)
            
            logger.info(f"Added profile: {person.name} ({normalized_url})")
            
        except Exception as e:
            logger.error(f"Failed to add profile {person.linkedin_url}: {e}")
    
    def _normalize_url(self, url: str) -> str:
        """Normalize LinkedIn URL for consistent comparison"""
        if not url:
            return ""
        
        # Remove trailing slashes and query parameters
        parsed = urlparse(url)
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rstrip('/')}"
        
        # Remove common LinkedIn URL parameters
        if '?' in normalized:
            normalized = normalized.split('?')[0]
        
        return normalized
    
    def get_profile_count(self) -> int:
        """Get total number of scraped profiles"""
        return len(self.profiles)
    
    def export_to_excel(self, filename: str = None) -> str:
        """Export all profiles to Excel file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"linkedin_profiles_{timestamp}.xlsx"
        
        try:
            # Prepare data for Excel export
            excel_data = []
            
            for url, profile in self.profiles.items():
                # Flatten the nested data structure
                row = {
                    'LinkedIn URL': profile.get('linkedin_url', ''),
                    'Name': profile.get('name', ''),
                    'Current Company': profile.get('company', ''),
                    'Current Job Title': profile.get('job_title', ''),
                    'About': ' '.join(profile.get('about', [])) if profile.get('about') else '',
                    'Scraped At': profile.get('scraped_at', ''),
                    'Total Experiences': len(profile.get('experiences', [])),
                    'Total Education': len(profile.get('educations', [])),
                    'Total Contacts': len(profile.get('contacts', [])),
                    'Interests': ', '.join(profile.get('interests', [])),
                }
                
                # Add experience details
                experiences = profile.get('experiences', [])
                for i, exp in enumerate(experiences[:3]):  # Limit to first 3 experiences
                    prefix = f"Experience_{i+1}_"
                    row[f"{prefix}Position"] = exp.get('position_title', '')
                    row[f"{prefix}Company"] = exp.get('institution_name', '')
                    row[f"{prefix}Duration"] = exp.get('duration', '')
                    row[f"{prefix}Location"] = exp.get('location', '')
                    row[f"{prefix}Description"] = exp.get('description', '')
                
                # Add education details
                educations = profile.get('educations', [])
                for i, edu in enumerate(educations[:2]):  # Limit to first 2 educations
                    prefix = f"Education_{i+1}_"
                    row[f"{prefix}Institution"] = edu.get('institution_name', '')
                    row[f"{prefix}Degree"] = edu.get('degree', '')
                    row[f"{prefix}Duration"] = f"{edu.get('from_date', '')} - {edu.get('to_date', '')}"
                
                excel_data.append(row)
            
            # Create DataFrame and export to Excel
            df = pd.DataFrame(excel_data)
            df.to_excel(filename, index=False, engine='openpyxl')
            
            logger.info(f"Exported {len(excel_data)} profiles to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to export to Excel: {e}")
            raise


class LinkedInProfileDiscovery:
    """Discovers new LinkedIn profiles through various methods"""
    
    def __init__(self, driver):
        self.driver = driver
        self.discovered_urls: Set[str] = set()
    
    def discover_from_company_employees(self, company_urls: List[str], max_profiles: int = 20) -> List[str]:
        """Discover profiles by browsing company employee pages"""
        discovered = []
        
        for company_url in company_urls:
            try:
                # Navigate to company people page
                people_url = f"{company_url.rstrip('/')}/people/"
                self.driver.get(people_url)
                time.sleep(random.uniform(3, 6))
                
                # Find employee profile links
                profile_links = self._extract_profile_links()
                discovered.extend(profile_links[:max_profiles])
                
                if len(discovered) >= max_profiles:
                    break
                    
            except Exception as e:
                logger.warning(f"Failed to discover from company {company_url}: {e}")
                continue
        
        return discovered[:max_profiles]
    
    def discover_from_connections(self, seed_profiles: List[str], max_profiles: int = 20) -> List[str]:
        """Discover profiles through 'People Also Viewed' sections"""
        discovered = []
        
        for profile_url in seed_profiles:
            try:
                self.driver.get(profile_url)
                time.sleep(random.uniform(3, 6))
                
                # Look for "People also viewed" section
                try:
                    also_viewed_section = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//section[contains(@class, 'pv-browsemap-section')]"))
                    )
                    
                    profile_links = also_viewed_section.find_elements(By.XPATH, ".//a[contains(@href, '/in/')]")
                    
                    for link in profile_links[:5]:  # Limit per profile
                        href = link.get_attribute('href')
                        if href and '/in/' in href and href not in self.discovered_urls:
                            discovered.append(href)
                            self.discovered_urls.add(href)
                            
                except (TimeoutException, NoSuchElementException):
                    logger.debug(f"No 'also viewed' section found for {profile_url}")
                
                if len(discovered) >= max_profiles:
                    break
                    
            except Exception as e:
                logger.warning(f"Failed to discover from profile {profile_url}: {e}")
                continue
        
        return discovered[:max_profiles]
    
    def discover_from_search(self, search_terms: List[str], max_profiles: int = 20) -> List[str]:
        """Discover profiles through LinkedIn search"""
        discovered = []
        
        for term in search_terms:
            try:
                # Navigate to LinkedIn search
                search_url = f"https://www.linkedin.com/search/results/people/?keywords={term.replace(' ', '%20')}"
                self.driver.get(search_url)
                time.sleep(random.uniform(4, 7))
                
                # Extract profile links from search results
                profile_links = self._extract_profile_links()
                discovered.extend(profile_links[:10])  # Limit per search term
                
                if len(discovered) >= max_profiles:
                    break
                    
            except Exception as e:
                logger.warning(f"Failed to search for '{term}': {e}")
                continue
        
        return discovered[:max_profiles]
    
    def _extract_profile_links(self) -> List[str]:
        """Extract LinkedIn profile links from current page"""
        links = []
        try:
            # Find all LinkedIn profile links
            profile_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/in/')]")
            
            for element in profile_elements:
                try:
                    href = element.get_attribute('href')
                    if href and '/in/' in href and href not in self.discovered_urls:
                        # Clean URL
                        clean_url = href.split('?')[0].rstrip('/')
                        if clean_url not in links:
                            links.append(clean_url)
                            self.discovered_urls.add(clean_url)
                except StaleElementReferenceException:
                    continue
                    
        except Exception as e:
            logger.warning(f"Failed to extract profile links: {e}")
        
        return links


class EnhancedLinkedInScraper:
    """Enhanced LinkedIn scraper with random profile discovery and Excel export"""
    
    def __init__(self, headless: bool = False, use_proxy: bool = False):
        self.headless = headless
        self.use_proxy = use_proxy
        self.driver = None
        self.profile_db = ProfileDatabase()
        self.discovery = None
        
        # Initialize UserAgent with fallback
        if HAS_FAKE_USERAGENT:
            self.ua = UserAgent()
        else:
            self.ua = UserAgent()  # Uses our fallback class
        
    def _setup_driver(self):
        """Setup Chrome WebDriver with optimized settings"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Stealth options
        chrome_options.add_argument(f"--user-agent={self.ua.random}")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")  # Faster loading
        
        # Suppress verbose logging and errors
        chrome_options.add_argument("--log-level=3")  # Suppress INFO, WARNING, ERROR
        chrome_options.add_argument("--silent")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-dev-tools")
        chrome_options.add_argument("--disable-gpu-logging")
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-client-side-phishing-detection")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--disable-translate")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("--mute-audio")
        
        # Suppress additional Chrome errors
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        
        # Window size
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            # Use webdriver-manager to handle ChromeDriver automatically
            service = Service(ChromeDriverManager().install())
            
            # Suppress ChromeDriver logs
            service.creation_flags = 0x08000000  # CREATE_NO_WINDOW on Windows
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("ChromeDriver initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromeDriver: {e}")
            raise
    
    def login(self, email: str = None, password: str = None):
        """Login to LinkedIn"""
        if not self.driver:
            self._setup_driver()
        
        try:
            actions.login(self.driver, email, password)
            logger.info("Successfully logged into LinkedIn")
            
            # Initialize discovery after login
            self.discovery = LinkedInProfileDiscovery(self.driver)
            
        except Exception as e:
            logger.error(f"Failed to login to LinkedIn: {e}")
            raise
    
    def scrape_profile(self, linkedin_url: str, max_retries: int = 3) -> Optional[Person]:
        """Scrape a single LinkedIn profile with retry logic"""
        if self.profile_db.is_scraped(linkedin_url):
            logger.info(f"Profile already scraped: {linkedin_url}")
            return None
        
        retries = 0
        while retries < max_retries:
            try:
                logger.info(f"Scraping profile: {linkedin_url} (attempt {retries + 1})")
                
                # Random delay to avoid rate limiting
                time.sleep(random.uniform(2, 5))
                
                # Scrape the profile
                person = Person(
                    linkedin_url=linkedin_url,
                    driver=self.driver,
                    scrape=True,
                    close_on_complete=False
                )
                
                if person.name:  # Successful scrape
                    self.profile_db.add_profile(person)
                    logger.info(f"Successfully scraped: {person.name}")
                    return person
                else:
                    logger.warning(f"No data found for profile: {linkedin_url}")
                    return None
                    
            except Exception as e:
                retries += 1
                logger.warning(f"Attempt {retries} failed for {linkedin_url}: {e}")
                
                if retries < max_retries:
                    time.sleep(random.uniform(5, 10))  # Wait before retry
                else:
                    logger.error(f"Failed to scrape {linkedin_url} after {max_retries} attempts")
        
        return None
    
    def discover_and_scrape(self, 
                          seed_profiles: List[str] = None,
                          company_urls: List[str] = None,
                          search_terms: List[str] = None,
                          max_profiles: int = 50,
                          export_interval: int = 10):
        """Discover new profiles and scrape them"""
        
        if not self.driver:
            raise ValueError("Please login first before scraping")
        
        discovered_urls = set()
        scraped_count = 0
        
        # Discover profiles using various methods
        if seed_profiles:
            logger.info("Discovering profiles from connections...")
            urls = self.discovery.discover_from_connections(seed_profiles, max_profiles // 3)
            discovered_urls.update(urls)
        
        if company_urls:
            logger.info("Discovering profiles from companies...")
            urls = self.discovery.discover_from_company_employees(company_urls, max_profiles // 3)
            discovered_urls.update(urls)
        
        if search_terms:
            logger.info("Discovering profiles from search...")
            urls = self.discovery.discover_from_search(search_terms, max_profiles // 3)
            discovered_urls.update(urls)
        
        # Filter out already scraped profiles
        new_urls = [url for url in discovered_urls if not self.profile_db.is_scraped(url)]
        
        logger.info(f"Discovered {len(discovered_urls)} total URLs, {len(new_urls)} new ones")
        
        # Randomize order
        random.shuffle(new_urls)
        
        # Scrape profiles
        for i, url in enumerate(new_urls[:max_profiles]):
            try:
                person = self.scrape_profile(url)
                
                if person:
                    scraped_count += 1
                    
                    # Export to Excel periodically
                    if scraped_count % export_interval == 0:
                        self.export_to_excel()
                        self.profile_db.save_database()
                
                # Random delay between profiles
                time.sleep(random.uniform(3, 8))
                
            except KeyboardInterrupt:
                logger.info("Scraping interrupted by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error while scraping {url}: {e}")
                continue
        
        # Final export and save
        logger.info(f"Scraping completed. Total profiles scraped: {scraped_count}")
        self.export_to_excel()
        self.profile_db.save_database()
    
    def export_to_excel(self, filename: str = None) -> str:
        """Export all scraped profiles to Excel"""
        return self.profile_db.export_to_excel(filename)
    
    def get_stats(self) -> Dict:
        """Get scraping statistics"""
        return {
            'total_profiles': self.profile_db.get_profile_count(),
            'database_file': self.profile_db.db_file
        }
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            logger.info("Driver closed")


def main():
    """Main function to run the enhanced scraper"""
    
    # Configuration
    HEADLESS = False  # Set to True for headless browsing
    MAX_PROFILES = 30  # Number of profiles to scrape
    
    # Sample data for discovery
    SEED_PROFILES = [
        "https://www.linkedin.com/in/satyanadella/",
        "https://www.linkedin.com/in/sundarpichai/",
        "https://www.linkedin.com/in/jeffweiner08/"
    ]
    
    COMPANY_URLS = [
        "https://www.linkedin.com/company/microsoft/",
        "https://www.linkedin.com/company/google/",
        "https://www.linkedin.com/company/apple/"
    ]
    
    SEARCH_TERMS = [
        "Software Engineer",
        "Data Scientist", 
        "Product Manager",
        "Marketing Manager"
    ]
    
    scraper = EnhancedLinkedInScraper(headless=HEADLESS)
    
    try:
        # Login (will prompt for credentials if not provided)
        scraper.login()
        
        # Start discovery and scraping
        scraper.discover_and_scrape(
            seed_profiles=SEED_PROFILES,
            company_urls=COMPANY_URLS,
            search_terms=SEARCH_TERMS,
            max_profiles=MAX_PROFILES,
            export_interval=5
        )
        
        # Print final statistics
        stats = scraper.get_stats()
        print(f"\n=== Scraping Complete ===")
        print(f"Total profiles scraped: {stats['total_profiles']}")
        print(f"Database file: {stats['database_file']}")
        
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
    finally:
        scraper.cleanup()


if __name__ == "__main__":
    main()
