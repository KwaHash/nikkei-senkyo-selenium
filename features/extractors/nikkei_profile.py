import os
import re
from typing import Any, Dict, List

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from features.config import AVATARS_DIR, DEFAULT_WAIT_TIME
from features.utils import (
	download_image,
	fullwidth_digits_to_halfwidth,
	generate_image_filename,
	get_image_extension,
	normalize_image_url,
)


class NikkeiProfileExtractor:
	def __init__(self, wait_time: int = DEFAULT_WAIT_TIME):
		self.wait_time = wait_time

	def extract(self, driver, href: str) -> Dict[str, Any]:
		wait = WebDriverWait(driver, self.wait_time)
		result = self._get_default_result()
		try:
			driver.get(href)
			wait.until(EC.presence_of_element_located((By.CLASS_NAME, "personSection_pyxsugc")))
			section = driver.find_element(By.CLASS_NAME, "personSection_pyxsugc")

			self._extract_name(section, result)
			self._extract_party(section, result)
			self._extract_district_proportional(section, result)
			self._extract_election_count(section, result)
			self._extract_birth_date(driver, result)
			self._extract_avatar(driver, section, href, result)

			wait.until(EC.presence_of_element_located((By.CLASS_NAME, "politicsSection_pr8krom")))
			politics_section = driver.find_element(By.CLASS_NAME, "politicsSection_pr8krom")
			self._extract_politics(politics_section, result)
			self._extract_questions_answers(driver, result)
		except Exception:
			pass
		return result

	def _get_default_result(self) -> Dict[str, Any]:
		return {
			"kanji_name": "",
			"hiragana_name": "",
			"party": None,
			"district": None,
			"proportional": None,
			"shu_count": 0,
			"san_count": 0,
			"birth_date": None,
			"avatar": None,
			"title": None,
			"biography": None,
			"origin": None,
			"shin": None,
			"questions_answers": [],
		}

	def _extract_name(self, section, result: Dict[str, Any]) -> None:
		try:
			kanji = section.find_element(By.CLASS_NAME, "personName_pui2ow9")
			hiragana = section.find_element(By.CLASS_NAME, "personNameHiragana_ppmkyx2")
			result["kanji_name"] = kanji.text.strip()
			result["hiragana_name"] = hiragana.text.strip()
		except Exception:
			pass

	def _extract_party(self, section, result: Dict[str, Any]) -> None:
		try:
			party = section.find_element(By.ID, "person_detail_party")
			result["party"] = party.text.strip() or None
		except Exception:
			pass

	def _extract_district_proportional(self, section, result: Dict[str, Any]) -> None:
		try:
			el = section.find_element(By.ID, "person_detail_district_name")
			raw = (el.text or "").strip()
			if not raw:
				pass
			elif "（比例：" in raw:
				# e.g. "-（比例：北海道）" -> district empty, proportional = "北海道"
				result["district"] = ""
				match = re.search(r"比例：(.*?)）", raw)
				result["proportional"] = match.group(1).strip() if match else None
			elif "（比例重複）" in raw:
				# e.g. "青森１区（比例重複）" -> district = "青森1区", proportional = "比例重複"
				district_str = raw.replace("（比例重複）", "").strip() or raw
				result["district"] = fullwidth_digits_to_halfwidth(district_str)
				result["proportional"] = "比例重複"
			else:
				result["district"] = fullwidth_digits_to_halfwidth(raw)
		except Exception:
			pass

	def _extract_election_count(self, section, result: Dict[str, Any]) -> None:
		try:
			elements = section.find_elements(By.CLASS_NAME, "basicInfoItemData_b7tm3ia")
			if len(elements) < 3:
				return
			election_text = (elements[2].text or "").strip()
			if election_text:
				shu_match = re.search(r"衆：(\d+)回", election_text)
				if shu_match:
					result["shu_count"] = int(shu_match.group(1))
				san_match = re.search(r"参：(\d+)回", election_text)
				if san_match:
					result["san_count"] = int(san_match.group(1))
		except Exception:
			pass

	def _extract_birth_date(self, driver, result: Dict[str, Any]) -> None:
		try:
			elements = driver.find_elements(By.CLASS_NAME, "basicInfoItemData_b7tm3ia")
			if len(elements) < 4:
				return
			birth_text = (elements[3].text or "").strip()
			birth_match = re.match(r"(\d{4}/\d{2}/\d{2})", birth_text)
			if birth_match:
				result["birth_date"] = birth_match.group(1)
		except Exception:
			pass

	def _extract_avatar(
		self, driver, section, href: str, result: Dict[str, Any]
	) -> None:
		try:
			img = section.find_element(By.CLASS_NAME, "container_c1dnlfyj").find_element(
				By.TAG_NAME, "img"
			)
			image_src = img.get_attribute("data-src") or img.get_attribute("src")
			if not image_src:
				return
			image_src = image_src.strip()
			os.makedirs(AVATARS_DIR, exist_ok=True)
			base = generate_image_filename(result["kanji_name"], href)
			ext = get_image_extension(image_src)
			filename = f"{base}{ext}"
			path = os.path.join(AVATARS_DIR, filename)
			image_src = normalize_image_url(image_src, driver.current_url)
			if download_image(image_src, path):
				result["avatar"] = os.path.join(f"/{AVATARS_DIR}", filename).replace("\\", "/")
		except Exception:
			pass

	def _extract_politics(self, section, result: Dict[str, Any]) -> None:
		try:
			elements = section.find_elements(By.CLASS_NAME, "emphasisItemValue_e1nfyxx1")
			if len(elements) >= 2:
				result["title"] = elements[0].text.strip()
				result["biography"] = elements[1].text.strip()
			origin_text = section.find_element(By.CLASS_NAME, "leftItemValue_l1x2n5ly").text.strip()
			result["origin"] = "" if origin_text == "-" else origin_text
			result["shin"] = section.find_element(
				By.CLASS_NAME, "rightItemValue_rq2m1jb"
			).text.strip()
		except Exception:
			pass

	def _extract_questions_answers(self, driver, result: Dict[str, Any]) -> None:
		try:
			qa_container = driver.find_element(By.CLASS_NAME, "QuestionAndAnswers")
			qa_items = qa_container.find_elements(By.CLASS_NAME, "questionAndAnswer_q7k5q99")
			questions_answers: List[Dict[str, str]] = []
			for qa_item in qa_items:
				try:
					question_elem = qa_item.find_element(By.CLASS_NAME, "question_q1onur46")
					question = question_elem.text.strip()
					selected_answer = None
					choice_elements = qa_item.find_elements(By.CLASS_NAME, "choice_c19a7iwb")
					for choice in choice_elements:
						if "choiceHighlight_c1qfqact" in (choice.get_attribute("class") or ""):
							selected_answer = choice.text.strip()
							break
					if question and selected_answer:
						questions_answers.append({"question": question, "answer": selected_answer})
				except Exception:
					continue
			result["questions_answers"] = questions_answers
		except Exception:
			pass
