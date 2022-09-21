import os
from pathlib import Path

PERIOD = int(os.getenv("SITE_VISIT_PERIOD", 1))
URLS = os.getenv("URLS").split(",")
USE_PROXY = os.getenv("USE_PROXY", "true").lower() == "true"

LOG_LEVEL = os.getenv("LOG_LEVEL",'info').upper()

PARALLELS = int(os.getenv("PARALLELS", 1))

BASE_DIR = Path(__file__).resolve().parent

RUN_HEADLESS = os.getenv("RUN_HEADLESS","False").lower() == "true"