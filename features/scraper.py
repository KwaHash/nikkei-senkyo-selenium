from features.extractors import (
	NikkieCandidateExtractor,
	NikkieProportionCandidateExtractor,
	NikkeiProfileExtractor,
	SenkyoCandidateTableExtractor,
	SenkyoDistrictNavigationExtractor,
	SenkyoProfileSiteLinksExtractor,
)
from features.config import DEFAULT_WAIT_TIME

def extract_senkyo_district_nav_links(driver, wait_time=DEFAULT_WAIT_TIME):
	extractor = SenkyoDistrictNavigationExtractor(wait_time=wait_time)
	return extractor.extract(driver)

def extract_senkyo_table_candidates(driver, wait_time=DEFAULT_WAIT_TIME):
	extractor = SenkyoCandidateTableExtractor(wait_time=wait_time)
	return extractor.extract(driver)

def extract_senkyo_profile_info(driver, href, wait_time=DEFAULT_WAIT_TIME):
	extractor = SenkyoProfileSiteLinksExtractor(wait_time=wait_time)
	return extractor.extract(driver, href)

def extract_nikkie_candidate_links(driver, wait_time=DEFAULT_WAIT_TIME):
	extractor = NikkieCandidateExtractor(wait_time=wait_time)
	return extractor.extract(driver)

def extract_nikkie_proportion_candidate_links(driver, wait_time=DEFAULT_WAIT_TIME):
	extractor = NikkieProportionCandidateExtractor(wait_time=wait_time)
	return extractor.extract(driver)

def extract_profile_info(driver, href: str, wait_time=DEFAULT_WAIT_TIME):
	extractor = NikkeiProfileExtractor(wait_time=wait_time)
	return extractor.extract(driver, href)