from features.driver import create_driver
from features.scraper import extract_nikkie_proportion_candidate_links, extract_profile_info
from features.config import NIKKEI_SITE_BASE_URL
from features.database import insert_proportion_profile_info

def main():
	driver = create_driver(headless=True)
	blocks = ['北海道', '東北', '北関東', '南関東', '東京', '北陸信越', '東海', '近畿', '中国', '四国', '九州']
	
	try:
		for i in range(1, 12):
			url = f"{NIKKEI_SITE_BASE_URL}/hirei/{i:02d}"
			driver.get(url)
			candidates = extract_nikkie_proportion_candidate_links(driver)
			for item in candidates:
				profile = extract_profile_info(driver, item["href"])
				record_id = insert_proportion_profile_info(profile, item["rank"], blocks[i - 1])

	finally:
		driver.quit()


if __name__ == "__main__":
	main()
