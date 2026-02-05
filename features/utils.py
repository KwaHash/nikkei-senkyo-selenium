"""Utility functions for link labeling, filename sanitization, and image downloading."""

import re
import os
import urllib.request
import ssl
import hashlib
from urllib.parse import urlparse

def get_link_label(url):
	"""Determine label for a URL based on domain patterns."""
	url_lower = url.lower()
	
	if 'facebook.com' in url_lower:
		return 'facebook'
	elif 'youtube.com' in url_lower or 'youtu.be' in url_lower:
		return 'youtube'
	elif 'twitter.com' in url_lower or 'x.com' in url_lower:
		return 'twitter'
	elif 'instagram.com' in url_lower:
		return 'instagram'
	elif 'linkedin.com' in url_lower:
		return 'linkedin'
	elif 'tiktok.com' in url_lower:
		return 'tiktok'
	elif 'line.me' in url_lower:
		return 'line'
	elif 'note.com' in url_lower:
		return 'note'
	elif 'ameblo.jp' in url_lower:
		return 'ameblo'
	else:
		return 'homepage'


def fullwidth_digits_to_halfwidth(s: str) -> str:
	if not s:
		return s
	trans = str.maketrans('０１２３４５６７８９', '0123456789')
	return s.translate(trans)


def sanitize_filename(filename):
	"""Sanitize filename by removing invalid characters."""
	# Remove invalid characters for filenames
	filename = re.sub(r'[<>:"/\\|?*]', '', filename)
	# Replace spaces with underscores
	filename = filename.replace(' ', '_')
	# Remove multiple consecutive underscores
	filename = re.sub(r'_+', '_', filename)
	return filename.strip('_')


def download_image(image_url, save_path):
	"""Download image from URL to specified path."""
	try:
		# Create an SSL context that doesn't verify certificates
		# This is needed for some sites with certificate issues
		ssl_context = ssl.create_default_context()
		ssl_context.check_hostname = False
		ssl_context.verify_mode = ssl.CERT_NONE
		
		# Open URL with SSL context and write to file
		with urllib.request.urlopen(image_url, context=ssl_context) as response:
			with open(save_path, 'wb') as out_file:
				out_file.write(response.read())
		return True
	except Exception as e:
		print(f"Error downloading image from {image_url}: {e}")
		return False


def normalize_image_url(image_src, current_url):
	"""Convert relative image URLs to absolute URLs."""
	if image_src.startswith('//'):
		return 'https:' + image_src
	elif image_src.startswith('/'):
		# Get base URL from current page
		base_url = f"{urlparse(current_url).scheme}://{urlparse(current_url).netloc}"
		return base_url + image_src
	return image_src


def get_image_extension(image_src):
	"""Extract file extension from image URL."""
	parsed_url = urlparse(image_src)
	path = parsed_url.path
	ext = os.path.splitext(path)[1] if os.path.splitext(path)[1] else '.jpg'
	# Remove query parameters from extension
	ext = ext.split('?')[0] if '?' in ext else ext
	if not ext or ext == '.':
		ext = '.jpg'
	return ext


def generate_image_filename(name, href):
	"""Generate a safe filename for the image."""
	if name:
		base_filename = sanitize_filename(name)
	else:
		base_filename = hashlib.md5(href.encode()).hexdigest()
	return base_filename

def longest_common_subsequence(str1: str, str2: str) -> int:
	"""Calculate the length of the longest common subsequence (LCS) between two strings."""
	# Remove spaces for comparison
	str1_clean = str1.replace(' ', '')
	str2_clean = str2.replace(' ', '')
	
	m, n = len(str1_clean), len(str2_clean)
	
	# Create a DP table to store LCS lengths
	dp = [[0] * (n + 1) for _ in range(m + 1)]
	
	# Fill the DP table
	for i in range(1, m + 1):
		for j in range(1, n + 1):
			if str1_clean[i - 1] == str2_clean[j - 1]:
				dp[i][j] = dp[i - 1][j - 1] + 1
			else:
				dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
	
	return dp[m][n]