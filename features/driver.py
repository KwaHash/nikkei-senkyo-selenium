"""WebDriver setup and configuration."""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def create_driver(headless=True):
	"""Create and configure Chrome WebDriver."""
	chrome_options = Options()
	if headless:
		chrome_options.add_argument("--headless")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument("--disable-dev-shm-usage")
	
	service = Service(ChromeDriverManager().install())
	driver = webdriver.Chrome(service=service, options=chrome_options)
	return driver
