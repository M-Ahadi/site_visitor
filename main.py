import datetime
import logging
import os.path
import random
import sys
import re
import socket
import requests
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import configs
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(level=configs.LOG_LEVEL)
logger = logging.getLogger(__name__)

if not sys.platform.startswith('win'):
    from pyvirtualdisplay import Display

    display = Display(visible=False, size=(1024, 768))
    display.start()

proxy_list = []


def check_proxy(proxy):
    try:
        ip, port = proxy.split(":")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        result = sock.connect_ex((ip, int(port)))
        sock.close()
        return result
    except:
        return


def get_proxies():
    try:
        proxy_sites = [
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
            "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
            "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/socks5.txt",
            "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt",
            "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
            "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt",
            "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
            "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt"
        ]
        proxies = []
        for url in proxy_sites:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    match = re.findall(r'[0-9]+(?:\.[0-9]+){3}:[0-9]+', response.text)
                    proxies += match
            except Exception as e:
                logger.error(e)
        proxies = list(set(proxies))
        random.shuffle(proxies)
        logger.info("{} proxy is found".format(len(proxies)))
        return proxies
    except Exception as e:
        logger.error(e)


def config_chrome():
    chrome_options = webdriver.ChromeOptions()
    if configs.RUN_HEADLESS:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    if not sys.platform.startswith('win'):
        chrome_options.binary_location = "/usr/bin/google-chrome"
    chrome_options.add_argument("--disable-dev-shm-usage")
    if configs.USE_PROXY:
        proxy = random.choice(available_proxies)
        chrome_options.add_argument('--proxy-server=%s' % proxy)
        logger.info(f"visited website with proxy: {str(proxy)}")
    return chrome_options


def visit_site(web_urls, parallel_state, driver=None):
    web_urls.append(web_urls.pop(0))
    web_url = web_urls[0]
    if configs.PARALLELS > 1:
        logger.info(f"parallel number {parallel_state} visiting {web_url} at {datetime.datetime.now()}")
    else:
        logger.info(f"visiting {web_url} at {datetime.datetime.now()}")
    try:
        if driver:
            driver.close()
        driver = webdriver.Chrome(service=Service(os.path.join(configs.BASE_DIR, "chromedriver")),
                                  options=config_chrome())
        driver.get(web_url)
        WebDriverWait(driver, random.randint(int(os.getenv("MINIMUM_VISIT", 10)), int(os.getenv("MAXIMUM_VISIT", 100))))
    except Exception as e:
        logger.error(e)
    loop.call_later(configs.PERIOD, visit_site, web_urls, parallel_state, driver)


def update_available_proxies(proxy_list_to_check, proxy_index, count_need=-1):
    proxies_count = len(proxy_list_to_check)
    printed = False
    for i in range(proxy_index, proxies_count):
        if len(available_proxies) % 100 == 0 and not printed and len(available_proxies) > 0:
            printed = True
            logger.info("Found {} available".format(i, proxies_count, len(available_proxies)))

        if len(available_proxies) % 100 > 0:
            printed = False
        if check_proxy(proxy_list_to_check[i]):
            available_proxies.append(proxy_list_to_check[i])

        if len(available_proxies) == configs.PARALLELS and count_need > 0:
            return i

    logger.info("Found {} available proxy.".format(len(available_proxies)))


if __name__ == "__main__":
    proxy_index = 0
    available_proxies = []
    loop = asyncio.get_event_loop()
    if not configs.URLS:
        logger.error("website url is not given.\nVariable URL should be configured")
        exit(-1)
    logger.info(f"Site visitor started for url: {configs.URLS}")
    if configs.USE_PROXY:
        logger.info("Proxy is enabled.")
        proxy_list = get_proxies()
        logger.info(f"checking available proxies")
        proxy_index = update_available_proxies(proxy_list, 0, count_need=configs.PARALLELS)

        if not proxy_list:
            logger.warning("no proxy found!!!")
            exit(-1)
    else:
        logger.info("Proxy is disabled.")

    for parallel in range(configs.PARALLELS):
        loop.call_soon(visit_site, configs.URLS, parallel + 1)

    if configs.USE_PROXY:
        loop.call_soon(update_available_proxies, proxy_list, proxy_index)
    loop.run_forever()
