import os

# Books to Scrape
BOOKS_BASE_URL = "https://books.toscrape.com"
HOME_URL = f"{BOOKS_BASE_URL}/index.html"
HOME_TITLE = "All products | Books to Scrape - Sandbox"

# Quotes to Scrape 
QUOTES_BASE_URL = "https://quotes.toscrape.com/"
QUOTES_LOGIN_URL = f"{QUOTES_BASE_URL}login"

QUOTES_HOME_TITLE = "Quotes to Scrape"
QUOTES_USERNAME = "admin"
QUOTES_PASSWORD = "admin"

# data sizing 
BOOKS_PER_PAGE = 20        
BOOKS_TO_SAMPLE = 5         
MAX_PAGES = 5                

# Timeouts
DEFAULT_TIMEOUT_MS = 10_000

#http codes
HTTP_OK = 200