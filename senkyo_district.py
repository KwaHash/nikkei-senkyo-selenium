from features.driver import create_driver
from features.scraper import (
	extract_senkyo_district_nav_links,
	extract_senkyo_table_candidates,
	extract_senkyo_profile_info
)
from features.config import SENKYO_DISTRICT_BASE_URL
from features.database import update_profile_website_info

def main():
	driver = create_driver(headless=True)
	
	try:
		for i in range(1, 48):
			url = f"{SENKYO_DISTRICT_BASE_URL}/{i}"
			driver.get(url)
		
			links = extract_senkyo_district_nav_links(driver)

			for j, item in enumerate(links, 1):
				print(f"{i}. District: {item['district']}")
				
				if item['link']:
					driver.get(item['link'])
					candidates_data = extract_senkyo_table_candidates(driver)

					for k, candidate_data in enumerate(candidates_data, 1):
						profile_info = extract_senkyo_profile_info(
							driver, 
							candidate_data['href'],
						)

						if profile_info and profile_info.get('name'):
							update_profile_website_info(profile_info['name'], profile_info['website'], item['district'])
						else:
							print(f"    Failed to insert profile: {profile_info} {item['district']}")
							
	finally:
		driver.quit()


if __name__ == "__main__":
	main()
