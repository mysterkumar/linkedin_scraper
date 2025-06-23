@echo off
echo Installing LinkedIn Scraper Dependencies...
echo.

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install required packages
echo Installing required packages...
pip install selenium>=4.15.0
pip install requests>=2.31.0
pip install lxml>=4.9.0
pip install pandas>=2.0.0
pip install openpyxl>=3.1.0
pip install webdriver-manager>=4.0.0
pip install fake-useragent>=1.4.0
pip install python-dotenv>=1.0.0
pip install tqdm>=4.66.0
pip install urllib3>=2.0.0

echo.
echo Installation complete!
echo.
echo You can now run the scraper with:
echo   python simple_scraper.py
echo.
pause
