import os
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_TOKEN=os.getenv("TELEGRAM_TOKEN","")
CHAT_ID=int(os.getenv("CHAT_ID","588505226"))
POLL_SECONDS=int(os.getenv("POLL_SECONDS","60"))
MAX_TOKEN_AGE_MINUTES=int(os.getenv("MAX_TOKEN_AGE_MINUTES","30"))
MIN_LIQUIDITY_USD=float(os.getenv("MIN_LIQUIDITY_USD","10000"))
MIN_VOLUME_5M_USD=float(os.getenv("MIN_VOLUME_5M_USD","2500"))
MIN_SCORE=float(os.getenv("MIN_SCORE","75"))
TREND_FEEDS=[x.strip() for x in os.getenv("TREND_FEEDS","").split(",") if x.strip()]
DB_PATH=os.getenv("DB_PATH","radar.sqlite3")
