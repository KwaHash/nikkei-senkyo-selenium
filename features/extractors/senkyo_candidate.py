from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.config import PARTIES
from typing import List, Dict

from features.config import DEFAULT_WAIT_TIME


class SenkyoCandidateTableExtractor:
	def __init__(self, wait_time: int = DEFAULT_WAIT_TIME):
		self.wait_time = wait_time
	
	def extract(self, driver) -> List[Dict[str, str]]:
		wait = WebDriverWait(driver, self.wait_time)
		
		try:
			table_element = wait.until(
				EC.presence_of_element_located((By.CLASS_NAME, "m_senkyo_result_table"))
			)
			candidate_elements = table_element.find_elements(By.CLASS_NAME, "m_senkyo_result_data")
			
			candidates_data = []
			for candidate_element in candidate_elements:
				candidate_data = self._extract_candidate_data(candidate_element)
				if candidate_data and candidate_data.get('href'):
					candidates_data.append(candidate_data)
			
			return candidates_data
		except Exception as e:
			return []
	
	def _extract_candidate_data(self, candidate_element) -> Dict[str, str]:
		party = self._extract_party(candidate_element)
		new_comer = self._extract_new_comer(candidate_element)
		href = self._extract_href(candidate_element)
		
		return {
			'href': href,
			'party': party,
			'new_comer': new_comer
		}

	def _extract_party(self, candidate_element) -> str:
		try:
			party_element = candidate_element.find_element(By.CLASS_NAME, "m_senkyo_result_data_circle")
			party_text = party_element.text.strip()

			for party in PARTIES:
				if party in party_text:
					return party

		except Exception:
			pass
		
		return ""
	
	def _extract_new_comer(self, candidate_element) -> str:
		try:
			bottom_right = candidate_element.find_element(By.CLASS_NAME, "m_senkyo_result_data_bottom_right")
			para_elements = bottom_right.find_elements(By.CLASS_NAME, "m_senkyo_result_data_para")
			
			for para in para_elements:
				spans = para.find_elements(By.TAG_NAME, "span")
				if len(spans) >= 2:
					return spans[1].text.strip()
		except Exception:
			pass
		
		return ""
	
	def _extract_href(self, candidate_element) -> str:
		try:
			title_element = candidate_element.find_element(By.CLASS_NAME, "m_senkyo_result_data_ttl")
			anchor = title_element.find_element(By.TAG_NAME, "a")
			href = anchor.get_attribute("href")
			return href if href else ""
		except Exception:
			pass
		
		return ""
