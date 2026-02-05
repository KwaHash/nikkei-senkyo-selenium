from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict

from features.config import DEFAULT_WAIT_TIME


class SenkyoDistrictNavigationExtractor:
	def __init__(self, wait_time: int = DEFAULT_WAIT_TIME):
		self.wait_time = wait_time
	
	def extract(self, driver) -> List[Dict[str, str]]:
		wait = WebDriverWait(driver, self.wait_time)
		wrapper_element = wait.until(
			EC.presence_of_element_located((By.CLASS_NAME, "m_senkyo_block_wrapp"))
		)
		senkyo_elements = wrapper_element.find_elements(By.CLASS_NAME, "m_senkyo_block")
		
		links = []
		for senkyo_element in senkyo_elements:
			link_data = self._extract_link_from_li(senkyo_element)
			links.append(link_data)
		
		return links
	
	def _extract_link_from_li(self, senkyo_element) -> Dict[str, str]:
		text = ""
		link = ""
		
		try:
			title_element = senkyo_element.find_element(By.CLASS_NAME, "m_senkyo_block_ttl")
			anchor = title_element.find_element(By.TAG_NAME, "a")
			link = anchor.get_attribute("href")
			text = anchor.text.strip()
		except Exception:
			pass
		
		return {'district': text, 'link': link}
