from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict, List

from features.config import DEFAULT_WAIT_TIME
from features.utils import get_link_label

class SenkyoProfileSiteLinksExtractor:
	def __init__(self, wait_time: int = DEFAULT_WAIT_TIME):
		self.wait_time = wait_time
	
	def extract(self, driver, href: str) -> Dict:
		wait = WebDriverWait(driver, self.wait_time)
		
		try:
			driver.get(href)
			
			name = self._extract_name(driver, wait)
			site_links = self._extract_site_links(driver)
			
			return {
				'name': name,
				'website': site_links,
			}
		except Exception as e:
			return self._get_default_profile()
	
	def _extract_name(self, driver, wait: WebDriverWait) -> str:
		try:
			name_element = wait.until(
				EC.presence_of_element_located((By.CLASS_NAME, "p_seijika_profle_ttl"))
			)
			return name_element.text.strip()
		except Exception:
			return ""
	
	def _extract_site_links(self, driver) -> List[Dict[str, str]]:
		site_links = []
		
		try:
			sitelist_element = driver.find_element(By.CLASS_NAME, "p_seijika_profle_data_sitelist")
			anchor_elements = sitelist_element.find_elements(By.TAG_NAME, "a")
			
			for anchor in anchor_elements:
				link_url = anchor.get_attribute("href")
				if link_url:
					label = get_link_label(link_url)
					site_links.append({
						'label': label,
						'url': link_url
					})
		except Exception:
			# Element doesn't exist or no links found
			pass
		
		return site_links
	
	def _get_default_profile(self) -> Dict:
		return {
			'name': "",
			'website': None
		}
