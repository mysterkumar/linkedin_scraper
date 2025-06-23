# 🔐 How to Add Your LinkedIn Credentials

You have 2 options to add your LinkedIn credentials:

## Option 1: Environment Variables (.env file) - RECOMMENDED ✅

This is the most secure method as your credentials are stored in a separate file.

### Steps:

1. Open the `.env` file in this folder
2. Replace the placeholder values:
   ```
   LINKEDIN_EMAIL=your-actual-email@gmail.com
   LINKEDIN_PASSWORD=your-actual-password
   ```
3. Save the file
4. Run: `python launcher.py`

### Example .env file:

```
LINKEDIN_EMAIL=john.doe@gmail.com
LINKEDIN_PASSWORD=MySecurePassword123
MAX_PROFILES=50
HEADLESS_MODE=False
```

## Option 2: Direct in Code - CONVENIENT

### Steps:

1. Open `launcher_with_credentials.py`
2. Find these lines at the top:
   ```python
   LINKEDIN_EMAIL = "your-email@gmail.com"
   LINKEDIN_PASSWORD = "your-password"
   ```
3. Replace with your actual credentials:
   ```python
   LINKEDIN_EMAIL = "john.doe@gmail.com"
   LINKEDIN_PASSWORD = "MySecurePassword123"
   ```
4. Save the file
5. Run: `python launcher_with_credentials.py`

## ⚠️ Security Notes:

- **Option 1 (.env)** is more secure because:

  - Credentials are in a separate file
  - .env files are typically excluded from version control
  - Easier to manage and change credentials

- **Option 2 (direct)** is convenient but:
  - Credentials are in the code file
  - Risk of accidentally sharing credentials if you share the code

## 🚀 Quick Start After Setting Credentials:

### Using .env method:

```bash
python launcher.py
```

### Using direct credentials:

```bash
python launcher_with_credentials.py
```

### Or use the Windows batch file:

```bash
start_scraper.bat
```

## 🔒 Your credentials are safe:

- Only used to log into LinkedIn
- Never stored elsewhere or transmitted to third parties
- LinkedIn login happens directly through their official website
