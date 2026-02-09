from features.driver import create_driver
from features.scraper import extract_nikkie_result_pref, extract_profile_info
from features.config import NIKKEI_SITE_BASE_URL
from features.database import update_result_pref

def main_pref():
	driver = create_driver(headless=True)
	try:
		for i in range(1, 2):
			url = f"{NIKKEI_SITE_BASE_URL}/pref/{i:02d}"
			driver.get(url)
			links = extract_nikkie_result_pref(driver)
			for link in links:
				profile = extract_profile_info(driver, link["link"])
				update_result_pref(profile, link["is_elected"], link["vote_count"])

	finally:
		driver.quit()


if __name__ == "__main__":
	main_pref()
