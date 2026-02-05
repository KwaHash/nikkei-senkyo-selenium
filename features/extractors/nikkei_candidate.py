from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List

from features.config import DEFAULT_WAIT_TIME


class NikkieCandidateExtractor:
	LINK_TEXT = "略歴・政策の立場などをみる"

	def __init__(self, wait_time: int = DEFAULT_WAIT_TIME):
		self.wait_time = wait_time

	def extract(self, driver) -> List[str]:
		wait = WebDriverWait(driver, self.wait_time)
		wrapper = wait.until(
			EC.presence_of_element_located((By.CLASS_NAME, "senkyokuInfoContainer_sh483g9"))
		)
		anchors = self._find_profile_anchors(wrapper)
		return [a.get_attribute("href") for a in anchors if a.get_attribute("href")]

	def _find_profile_anchors(self, wrapper):
		anchors = []
		for el in wrapper.find_elements(By.TAG_NAME, "a"):
			if self.LINK_TEXT in (el.text or ""):
				anchors.append(el)
		return anchors
