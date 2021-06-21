import datetime
import logging
import os.path
import random
import sys

import requests
import asyncio
from selenium import webdriver
import configs

logging.basicConfig(level=configs.LOG_LEVEL)
logger = logging.getLogger(__name__)

if not sys.platform.startswith('win'):
    from pyvirtualdisplay import Display
    display = Display(visible=False, size=(1024, 768))
    display.start()


proxy_list = []


def get_proxies():
    proxies = requests.get("https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt")
    proxies = proxies.text.split("\n")[9:]
    proxies = [p.split(" ")[0] for p in proxies]
    return proxies


def config_chrome():
    chrome_options = webdriver.ChromeOptions()
    if configs.RUN_HEADLESS:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    if not sys.platform.startswith('win'):
        chrome_options.binary_location = "/usr/bin/google-chrome"
    chrome_options.add_argument("--disable-dev-shm-usage")
    if configs.USE_PROXY:
        proxy = random.choice(proxy_list)
        chrome_options.add_argument('--proxy-server=%s' % proxy)
        logger.info(f"visited website with proxy: {str(proxy)}")
    return chrome_options


def visit_site(web_url, parallel_state, driver=None):
    if configs.PARALLELS > 1:
        logger.info(f"parallel number {parallel_state} visiting {web_url} at {datetime.datetime.now()}")
    else:
        logger.info(f"visiting {web_url} at {datetime.datetime.now()}")
    try:
        if driver:
            driver.close()
        driver = webdriver.Chrome(executable_path=os.path.join(configs.BASE_DIR,"chromedriver"), options=config_chrome())
        driver.get(web_url)
    except Exception as e:
        logger.error(e)
    loop.call_later(configs.PERIOD, visit_site, web_url, parallel_state, driver)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    if not configs.URL:
        logger.error("website url is not given.\nVariable URL should be configured")
        exit(-1)
    logger.info(f"Site visitor started for url: {configs.URL}")
    if configs.USE_PROXY:
        proxy_list = get_proxies()
        logger.info("Proxy is enabled.")
    else:
        logger.info("Proxy is disabled.")
    for parallel in range(configs.PARALLELS):
        loop.call_soon(visit_site, configs.URL, parallel+1)
    loop.run_forever()
