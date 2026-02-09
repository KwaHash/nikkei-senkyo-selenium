from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Any, Dict, List

from features.config import DEFAULT_WAIT_TIME


class NikkieResultPrefExtractor:
	def __init__(self, wait_time: int = DEFAULT_WAIT_TIME):
		self.wait_time = wait_time

	def extract(self, driver) -> List[Dict[str, Any]]:
		wait = WebDriverWait(driver, self.wait_time)
		wrapper = wait.until(
			EC.presence_of_element_located((By.CLASS_NAME, "senkyokuInfoContainer_sh483g9"))
		)
		trs = []
		tbody_elements = wrapper.find_elements(By.TAG_NAME, "tbody")
		for tbody in tbody_elements:
			trs.extend(tbody.find_elements(By.TAG_NAME, "tr"))
		elected = []
		for i in range(0, len(trs) - 1, 2):
			data_tr, link_tr = trs[i], trs[i + 1]
			is_elected = self._has_tou(data_tr)
			link = self._get_profile_link_from_tr(link_tr)
			vote_count = self._get_vote_count_from_tr(data_tr)
			if link:
				elected.append({"link": link, "vote_count": vote_count, "is_elected": 1 if is_elected else 0})
		return elected

	def _has_tou(self, data_tr):
		"""True if this data row has 当 (elected for district)."""
		try:
			el = data_tr.find_element(By.XPATH, ".//*[contains(@class, 'dataTokakuCircleForSenkyoku')]")
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


	def _get_vote_count_from_tr(self, data_tr):
		"""Get vote count (票) from the data row. Returns int or 0."""
		try:
			el = data_tr.find_element(By.XPATH, ".//*[contains(@class, 'dataVoteCount')]")
			text = (el.text or "").replace("票", "").replace(",", "").strip()
			return int(text) if text.isdigit() else 0
		except Exception:
			return 0

