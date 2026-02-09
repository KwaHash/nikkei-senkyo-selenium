from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Any, Dict, List

from features.config import DEFAULT_WAIT_TIME


class NikkieResultHireiExtractor:
	def __init__(self, wait_time: int = DEFAULT_WAIT_TIME):
		self.wait_time = wait_time

	def extract(self, driver) -> List[Dict[str, Any]]:
		wait = WebDriverWait(driver, self.wait_time)
		wrapper = wait.until(
			EC.presence_of_element_located((By.CLASS_NAME, "hireiBlockContainer_h1wv1vqq"))
		)
		trs = []
		tables = wrapper.find_elements(By.CLASS_NAME, "pcCandidateList_p9ssem3")
		for table_element in tables:
			tbody_element = table_element.find_element(By.TAG_NAME, "tbody")
			trs.extend(tbody_element.find_elements(By.TAG_NAME, "tr"))
		elected = []
		for i in range(0, len(trs) - 1, 2):
			data_tr, link_tr = trs[i], trs[i + 1]
			is_elected = self._has_tou(data_tr)
			if not is_elected:
				continue
			link = self._get_profile_link_from_tr(link_tr)
			if link:
				elected.append({"link": link, "is_elected": 2 if is_elected else 0})
		return elected

	def _has_tou(self, data_tr):
		"""True if this data row has 当 (elected for district)."""
		try:
			el = data_tr.find_element(By.XPATH, ".//*[contains(@class, 'dataTokakuCircleForHirei_d6cikjq')]")
			return el and "当" in (el.text or "")
		except Exception:
			return False


	def _get_profile_link_from_tr(self, link_tr):
		"""Get profile href from the second tr (link row)."""
		try:
			a = link_tr.find_element(By.CSS_SELECTOR, "a[href*='person']")
			return (a.get_attribute("href") or "").strip() or None
		except Exception:
			return None

