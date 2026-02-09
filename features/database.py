import pymysql
import json
from typing import Optional
from features.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, QUESTION_ANSWER_REPLACEMENTS
from features.utils import longest_common_subsequence

myConnection = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    passwd=DB_PASSWORD, db=DB_NAME
)

def insert_profile_info(profile_info) -> Optional[int]:
	try:
		cursor = myConnection.cursor()
		
		kanji_name = profile_info.get('kanji_name') or ""
		hiragana_name = profile_info.get('hiragana_name') or ""
		party = profile_info.get('party') or None
		district = profile_info.get('district') or None
		proportional = profile_info.get('proportional') or None
		shu_count = profile_info.get('shu_count') or 0
		san_count = profile_info.get('san_count') or 0
		birth_date = profile_info.get('birth_date') or None
		avatar = profile_info.get('avatar') or None
		title = profile_info.get('title') or None
		biography = profile_info.get('biography') or None
		origin = profile_info.get('origin') or None
		shin = profile_info.get('shin') or None
		questions_answers = profile_info.get('questions_answers') or []
		questions_answers_json = json.dumps(questions_answers, ensure_ascii=False) if questions_answers else None
		
		create_table_sql = """
			CREATE TABLE IF NOT EXISTS representatives2026 (
				id INT AUTO_INCREMENT PRIMARY KEY,
				kanji_name VARCHAR(255),
				hiragana_name VARCHAR(255),
				party VARCHAR(255),
				district VARCHAR(255),
				proportional VARCHAR(255),
				rank INT,
				shu_count INT,
				san_count INT,
				birth_date VARCHAR(255),
				avatar VARCHAR(255),
				title VARCHAR(255),
				biography TEXT,
				origin VARCHAR(255),
				shin VARCHAR(255),
				questions_answers JSON,
				website JSON
			);
		"""
		cursor.execute(create_table_sql)

		sql = """
			INSERT INTO representatives2026
			(kanji_name, hiragana_name, party, district, proportional, shu_count, san_count, birth_date, avatar, title, biography, origin, shin, questions_answers)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
		"""
		
		values = (
			kanji_name,
			hiragana_name,
			party,
			district,
			proportional,
			shu_count,
			san_count,
			birth_date,
			avatar,
			title,
			biography,
			origin,
			shin,
			questions_answers_json
		)
		
		cursor.execute(sql, values)
		myConnection.commit()
		
		# Get the inserted record ID
		record_id = cursor.lastrowid
		cursor.close()
		
		return record_id
		
	except Exception as e:
		print(f"Error inserting profile info: {e}")
		myConnection.rollback()
		return None

def insert_proportion_profile_info(profile_info, rank: str, block: str) -> Optional[int]:
	try:
		cursor = myConnection.cursor()

		kanji_name = profile_info.get('kanji_name') or ""
		hiragana_name = profile_info.get('hiragana_name') or ""
		party = profile_info.get('party') or None
		district = profile_info.get('district') or None
		shu_count = profile_info.get('shu_count') or 0
		san_count = profile_info.get('san_count') or 0
		birth_date = profile_info.get('birth_date') or None
		avatar = profile_info.get('avatar') or None
		title = profile_info.get('title') or None
		biography = profile_info.get('biography') or None
		origin = profile_info.get('origin') or None
		shin = profile_info.get('shin') or None
		questions_answers = profile_info.get('questions_answers') or []
		questions_answers_json = json.dumps(questions_answers, ensure_ascii=False) if questions_answers else None

		select_sql = "SELECT id FROM representatives2026 WHERE kanji_name = %s AND district = %s LIMIT 1"
		cursor.execute(select_sql, (kanji_name, district))
		row = cursor.fetchone()

		if row:
			record_id = row[0]
			update_sql = "UPDATE representatives2026 SET proportional = %s, rank = %s WHERE id = %s"
			cursor.execute(update_sql, (block, rank, record_id))
			myConnection.commit()
			cursor.close()
			return record_id
		else:
			insert_sql = """
				INSERT INTO representatives2026
				(kanji_name, hiragana_name, party, district, proportional, rank, shu_count, san_count, birth_date, avatar, title, biography, origin, shin, questions_answers)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
			"""
			values = (
				kanji_name,
				hiragana_name,
				party,
				district,
				block,
				rank,
				shu_count,
				san_count,
				birth_date,
				avatar,
				title,
				biography,
				origin,
				shin,
				questions_answers_json
			)
			cursor.execute(insert_sql, values)
			myConnection.commit()
			record_id = cursor.lastrowid
			cursor.close()
			return record_id

	except Exception as e:
		print(f"Error in insert_proportion_profile_info: {e}")
		myConnection.rollback()
		return None

def update_profile_website_info(name: str, website: list[dict], district: str):
	try:
		cursor = myConnection.cursor(pymysql.cursors.DictCursor)

		if not name or not district:
			return None
		
		# Find all records with the same district
		sql = """
			SELECT p.id, p.kanji_name, p.hiragana_name
			FROM representatives2026 p
			WHERE p.district = %s AND p.kanji_name IS NOT NULL
		"""
		cursor.execute(sql, (district,))
		candidates = cursor.fetchall()
		
		if not candidates:
			print(f"No candidates found for district: {district}")
			return None
		
		# Find the best match using longest common subsequence
		best_match = None
		best_match_id = None
		max_lcs_length = 0
		
		for candidate in candidates:
			kanji_name = candidate.get('kanji_name', '')
			hiragana_name = candidate.get('hiragana_name', '')
			if not kanji_name:
				continue
			
			# Calculate LCS length
			lcs_length_kanji = longest_common_subsequence(name, kanji_name)
			lcs_length_hiragana = longest_common_subsequence(name, hiragana_name)
			
			# Update best match if this has a longer LCS
			if lcs_length_kanji > max_lcs_length or lcs_length_hiragana > max_lcs_length:
				max_lcs_length = max(lcs_length_kanji, lcs_length_hiragana)
				best_match = kanji_name if lcs_length_kanji > lcs_length_hiragana else hiragana_name
				best_match_id = candidate.get('id')
		
		if not best_match_id or max_lcs_length == 0:
			print(f"No matching candidate found for name: {name} in district: {district}")
			print(f"Available candidates: {[c.get('kanji_name') for c in candidates]}")
			return None
		else:
			pass # print(f"Name: {name} Best match: {best_match} id: {best_match_id}")
		
		# Convert website list to JSON string for storage in longtext field
		website_json = json.dumps(website, ensure_ascii=False) if website else None
		
		# Update the matched record with website
		update_sql = """
			UPDATE representatives2026
			SET website = %s
			WHERE id = %s
		"""
		cursor.execute(update_sql, (website_json, best_match_id))
		myConnection.commit()

		cursor.close()
		
		return best_match_id
		
	except Exception as e:
		print(f"Error updating profile info: {e}")
		myConnection.rollback()
		return None

def update_proportion_website_info(name: str, website: list[dict], block: str):
	try:
		cursor = myConnection.cursor(pymysql.cursors.DictCursor)

		if not name or not block:
			return None
		
		# Find all records with the same district
		sql = """
			SELECT p.id, p.kanji_name, p.hiragana_name
			FROM representatives2026 p
			WHERE p.proportional = %s AND p.kanji_name IS NOT NULL
		"""
		cursor.execute(sql, (block,))
		candidates = cursor.fetchall()
		
		if not candidates:
			print(f"No candidates found for district: {block}")
			return None
		
		# Find the best match using longest common subsequence
		best_match = None
		best_match_id = None
		max_lcs_length = 0
		
		for candidate in candidates:
			kanji_name = candidate.get('kanji_name', '')
			hiragana_name = candidate.get('hiragana_name', '')
			if not kanji_name:
				continue
			
			# Calculate LCS length
			lcs_length_kanji = longest_common_subsequence(name, kanji_name)
			lcs_length_hiragana = longest_common_subsequence(name, hiragana_name)
			
			# Update best match if this has a longer LCS
			if lcs_length_kanji > max_lcs_length or lcs_length_hiragana > max_lcs_length:
				max_lcs_length = max(lcs_length_kanji, lcs_length_hiragana)
				best_match = kanji_name if lcs_length_kanji > lcs_length_hiragana else hiragana_name
				best_match_id = candidate.get('id')
		
		if not best_match_id or max_lcs_length == 0:
			print(f"No matching candidate found for name: {name} in district: {block}")
			print(f"Available candidates: {[c.get('kanji_name') for c in candidates]}")
			return None
		else:
			pass # print(f"Name: {name} Best match: {best_match} id: {best_match_id}")
		
		# Convert website list to JSON string for storage in longtext field
		website_json = json.dumps(website, ensure_ascii=False) if website else None
		
		# Update the matched record with website
		update_sql = """
			UPDATE representatives2026
			SET website = %s
			WHERE id = %s
		"""
		cursor.execute(update_sql, (website_json, best_match_id))
		myConnection.commit()

		cursor.close()
		
		return best_match_id
		
	except Exception as e:
		print(f"Error updating profile info: {e}")
		myConnection.rollback()
		return None

def update_candidate_question():
	import json
	try:
		# Build old -> new lookup for quick replacement
		replacement = {p['old']: p['new'] for p in QUESTION_ANSWER_REPLACEMENTS}
		cursor = myConnection.cursor()
		cursor.execute(
			"SELECT id, questions_answers FROM representatives2026 WHERE questions_answers IS NOT NULL AND questions_answers != ''"
		)
		rows = cursor.fetchall()
		updated_rows = 0
		for row_id, qa_json in rows:
			if not qa_json:
				continue
			try:
				items = json.loads(qa_json) if isinstance(qa_json, str) else qa_json
			except (TypeError, json.JSONDecodeError):
				continue
			changed = False
			for item in items:
				if not isinstance(item, dict):
					continue
				q = item.get('question')
				a = item.get('answer')
				if q and q in replacement:
					item['question'] = replacement[q]
					changed = True
				if a and a in replacement:
					item['answer'] = replacement[a]
					changed = True
			if changed:
				new_json = json.dumps(items, ensure_ascii=False)
				cursor.execute(
					"UPDATE representatives2026 SET questions_answers = %s WHERE id = %s",
					(new_json, row_id)
				)
				updated_rows += cursor.rowcount
		myConnection.commit()
		cursor.close()
		print(f"questions_answers: updated {updated_rows} row(s) in representatives2026.")
	except Exception as e:
		print(f"Error updating questions_answers: {e}")
		myConnection.rollback()

def update_result_pref(profile_info, is_elected, vote_count):
	kanji_name = profile_info.get('kanji_name') or ""
	district = profile_info.get('district') or None
	shu_count = profile_info.get('shu_count') or 0

	cursor = myConnection.cursor(pymysql.cursors.DictCursor)

	if not kanji_name or not district:
		return None
	
	# Find all records with the same district
	sql = """
		SELECT p.id
		FROM representatives2026 p
		WHERE p.district = %s AND p.kanji_name = %s
	"""
	cursor.execute(sql, (district, kanji_name))
	row = cursor.fetchone()
	if not row:
		cursor.close()
		print(f"No candidates found for district: {district}")
		return None

	id_val = row["id"]
	update_sql = """
		UPDATE representatives2026
		SET shu_count = %s, vote_result = %s, vote_count = %s
		WHERE id = %s
	"""
	cursor.execute(update_sql, (shu_count, is_elected, vote_count, id_val))
	myConnection.commit()
	cursor.close()
	return id_val