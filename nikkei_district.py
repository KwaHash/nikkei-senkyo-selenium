from features.driver import create_driver
from features.scraper import extract_nikkie_candidate_links, extract_profile_info
from features.config import NIKKEI_SITE_BASE_URL
from features.database import insert_profile_info

def main():
	driver = create_driver(headless=True)
	
	total = 0
	try:
		for i in range(1, 48):
			url = f"{NIKKEI_SITE_BASE_URL}/pref/{i:02d}"
			driver.get(url)
			links = extract_nikkie_candidate_links(driver)
			total += len(links)
			# profile = extract_profile_info(driver, links[0])
			record_id = 0
			for link in links:
				profile = extract_profile_info(driver, link)
				record_id = insert_profile_info(profile)
			# print("i => ", i, total, record_id)

	finally:
		driver.quit()


if __name__ == "__main__":
	main()
