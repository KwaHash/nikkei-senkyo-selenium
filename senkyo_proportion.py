from features.driver import create_driver
from features.scraper import (
	extract_senkyo_proportion_nav_links,
	extract_senkyo_table_candidates,
	extract_senkyo_profile_info
)
from features.config import SENKYO_PROPORTION_BASE_URL
from features.database import update_proportion_website_info

def main():
	driver = create_driver(headless=True)
	blocks = ['北海道', '東北', '北関東', '南関東', '東京', '北陸信越', '東海', '近畿', '中国', '四国', '九州']
	
	try:
		for i in range(151, 152):
			url = f"{SENKYO_PROPORTION_BASE_URL}/{i}/hirei_party/4/candidates"
			driver.get(url)
		
			links = extract_senkyo_proportion_nav_links(driver)

			for j, link in enumerate(links, 1):
				
				if link:
					driver.get(link)
					candidates_data = extract_senkyo_table_candidates(driver)

					for k, candidate_data in enumerate(candidates_data, 1):
						profile_info = extract_senkyo_profile_info(
							driver, 
							candidate_data['href'],
						)

						if profile_info and profile_info.get('name'):
							record_id = update_proportion_website_info(profile_info['name'], profile_info['website'], blocks[i - 151])
						else:
							print(f"    Failed to insert profile: {profile_info} {blocks[i - 151]}")
							
	finally:
		driver.quit()


if __name__ == "__main__":
	main()
