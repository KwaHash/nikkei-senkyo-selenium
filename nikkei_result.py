from features.driver import create_driver
from features.scraper import extract_nikkie_result_pref, extract_nikkie_result_hirei, extract_profile_info
from features.config import NIKKEI_SITE_BASE_URL
from features.database import update_result_pref, update_result_hirei

def main_pref():
	driver = create_driver(headless=True)
	try:
		for i in range(1, 48):
			url = f"{NIKKEI_SITE_BASE_URL}/pref/{i:02d}"
			driver.get(url)
			links = extract_nikkie_result_pref(driver)
			for link in links:
				profile = extract_profile_info(driver, link["link"])
				update_result_pref(profile, link["is_elected"], link["vote_count"])

	finally:
		driver.quit()

def main_hirei():
	blocks = ['北海道', '東北', '北関東', '南関東', '東京', '北陸信越', '東海', '近畿', '中国', '四国', '九州']
	driver = create_driver(headless=True)
	try:
		for i in range(1, 12):
			url = f"{NIKKEI_SITE_BASE_URL}/hirei/{i:02d}"
			driver.get(url)
			candidates = extract_nikkie_result_hirei(driver)
			for item in candidates:
				profile = extract_profile_info(driver, item["link"])
				update_result_hirei(profile, blocks[i - 1], item["is_elected"])

	finally:
		driver.quit()


if __name__ == "__main__":
	# main_pref()
	main_hirei()
