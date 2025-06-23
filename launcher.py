#!/usr/bin/env python3
"""
LinkedIn Scraper Launcher
Clean interface to start the enhanced scraper
"""

import os
import sys
import getpass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    """Display welcome banner"""
    print("="*60)
    print("🚀 ENHANCED LINKEDIN SCRAPER")
    print("="*60)
    print("Features:")
    print("✅ Smart Profile Discovery")
    print("✅ Duplicate Prevention") 
    print("✅ Excel Export")
    print("✅ Rate Limiting Protection")
    print("✅ Error Recovery")
    print("="*60)

def get_credentials():
    """Get LinkedIn credentials from user or environment variables"""
    
    # Try to get credentials from environment variables first
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')
    
    if email and password:
        print("✅ Using credentials from .env file")
        print(f"📧 Email: {email}")
        return email, password
    
    # If not found in env, prompt user
    print("\\n📧 LinkedIn Login Required")
    print("Your credentials are only used to log into LinkedIn.")
    print("They are not stored or transmitted anywhere else.")
    print("\\n💡 Tip: You can save credentials in .env file to avoid typing them each time")
    print("-" * 40)
    
    email = input("LinkedIn Email: ").strip()
    password = getpass.getpass("LinkedIn Password: ")
    
    if not email or not password:
        print("❌ Email and password are required!")
        return None, None
    
    return email, password

def get_scraping_config():
    """Get scraping configuration from user"""
    print("\\n⚙️  Scraping Configuration")
    print("-" * 40)
    
    try:
        max_profiles = int(input("Max profiles to scrape (default 20): ") or "20")
        headless = input("Run in headless mode? (y/n, default n): ").lower().startswith('y')
        
        print("\\n🎯 Profile Discovery Methods:")
        print("1. Company employees (discovers from company pages)")
        print("2. Search terms (finds profiles by job titles)")
        print("3. Seed profiles (finds connections of known profiles)")
        
        methods = input("\\nSelect methods (1,2,3 or 'all', default 'all'): ").strip().lower()
        
        if methods == 'all' or not methods:
            use_companies = use_search = use_seeds = True
        else:
            use_companies = '1' in methods
            use_search = '2' in methods  
            use_seeds = '3' in methods
        
        return {
            'max_profiles': max_profiles,
            'headless': headless,
            'use_companies': use_companies,
            'use_search': use_search,
            'use_seeds': use_seeds
        }
        
    except ValueError:
        print("❌ Invalid input! Using defaults.")
        return {
            'max_profiles': 20,
            'headless': False,
            'use_companies': True,
            'use_search': True,
            'use_seeds': True
        }

def main():
    """Main launcher function"""
    
    clear_screen()
    show_banner()
    
    # Check imports
    try:
        from enhanced_scraper import EnhancedLinkedInScraper
        print("✅ Enhanced scraper loaded successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\\nPlease run: pip install -r requirements.txt")
        input("\\nPress Enter to exit...")
        return
    
    # Get credentials
    email, password = get_credentials()
    if not email or not password:
        input("\\nPress Enter to exit...")
        return
    
    # Get configuration
    config = get_scraping_config()
    
    print("\\n🚀 Starting Enhanced LinkedIn Scraper...")
    print("-" * 40)
    
    # Default discovery data
    seed_profiles = [
        "https://www.linkedin.com/in/satyanadella/",
        "https://www.linkedin.com/in/sundarpichai/",
        "https://www.linkedin.com/in/jeffweiner08/"
    ] if config['use_seeds'] else None
    
    company_urls = [
        "https://www.linkedin.com/company/microsoft/",
        "https://www.linkedin.com/company/google/",
        "https://www.linkedin.com/company/apple/"
    ] if config['use_companies'] else None
    
    search_terms = [
        "Software Engineer",
        "Data Scientist", 
        "Product Manager",
        "Marketing Manager"
    ] if config['use_search'] else None
    
    # Initialize and run scraper
    scraper = EnhancedLinkedInScraper(headless=config['headless'])
    
    try:
        print("📡 Connecting to LinkedIn...")
        scraper.login(email, password)
        
        print("🔍 Starting profile discovery and scraping...")
        print(f"Target: {config['max_profiles']} profiles")
        print("\\n" + "="*60)
        
        # Start scraping
        scraper.discover_and_scrape(
            seed_profiles=seed_profiles,
            company_urls=company_urls,
            search_terms=search_terms,
            max_profiles=config['max_profiles'],
            export_interval=5
        )
        
        # Show results
        stats = scraper.get_stats()
        print("\\n" + "="*60)
        print("🎉 SCRAPING COMPLETE!")
        print(f"📊 Total profiles scraped: {stats['total_profiles']}")
        print(f"💾 Database file: {stats['database_file']}")
        
        # Find Excel files
        excel_files = [f for f in os.listdir('.') if f.startswith('linkedin_profiles_') and f.endswith('.xlsx')]
        if excel_files:
            latest_excel = max(excel_files, key=os.path.getctime)
            print(f"📈 Excel file: {latest_excel}")
        
        print("="*60)
        
    except KeyboardInterrupt:
        print("\\n⚠️  Scraping interrupted by user")
    except Exception as e:
        print(f"\\n❌ Error: {e}")
        print("\\nTip: Try running with headless=False to see what's happening")
    finally:
        scraper.cleanup()
        input("\\nPress Enter to exit...")

if __name__ == "__main__":
    main()
