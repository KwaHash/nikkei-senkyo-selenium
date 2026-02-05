from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict, List

from features.config import DEFAULT_WAIT_TIME


class NikkieProportionCandidateExtractor:
	LINK_TEXT = "略歴・政策の立場などをみる"
	MEIBO_JUN_CLASS = "dataMeiboJun_d1y1nu5m"

	def __init__(self, wait_time: int = DEFAULT_WAIT_TIME):
		self.wait_time = wait_time

	def extract(self, driver) -> List[Dict[str, str]]:
		wait = WebDriverWait(driver, self.wait_time)
		wrapper = wait.until(
			EC.presence_of_element_located((By.CLASS_NAME, "hireiBlockContainer_h1wv1vqq"))
		)
		ranks = self._get_ranking_texts(wrapper)
		anchors = self._find_profile_anchors(wrapper)
		result = []
		for i, a in enumerate(anchors):
			href = a.get_attribute("href")
			if not href:
				continue
			result.append({"rank": ranks[i], "href": href})
		return result

	def _get_ranking_texts(self, wrapper) -> List[str]:
		"""Get text of all dataMeiboJun_d1y1nu5m elements in wrapper."""
		texts = []
		try:
			for el in wrapper.find_elements(By.CLASS_NAME, self.MEIBO_JUN_CLASS):
				texts.append((el.text or "").strip())
		except Exception:
			pass
		return texts

	def _find_profile_anchors(self, wrapper):
		anchors = []
		for el in wrapper.find_elements(By.TAG_NAME, "a"):
			if self.LINK_TEXT in (el.text or ""):
				anchors.append(el)
		return anchors
