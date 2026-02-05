import os
from dotenv import load_dotenv

load_dotenv()

PARTIES = [
	"自由民主党",
	"中道改革連合",
	"立憲民主党",
	"日本維新の会",
	"公明党",
	"国民民主党",
	"日本共産党",
	"れいわ新選組",
	"参政党",
	"日本保守党",
	"社会民主党",
	"チームみらい",
]

NIKKEI_SITE_BASE_URL = "https://www.nikkei.com/special/election/candidates"
SENKYO_SITE_BASE_URL = "https://go2senkyo.com/shugiin/28030/prefecture"
AVATARS_DIR = "avatars"
DEFAULT_WAIT_TIME = 1

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "civicmatch")
