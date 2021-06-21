import os

PERIOD = int(os.getenv("SITE_VISIT_PERIOD",1))
URL = os.getenv("URL")
USE_PROXY = os.getenv("USE_PROXY","False").lower() == "true"

LOG_LEVEL = os.getenv("LOG_LEVEL").upper()

PARALLELS = int(os.getenv("PARALLELS",1))
