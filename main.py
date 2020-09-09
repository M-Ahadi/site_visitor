import random

import requests
import asyncio
from selenium.webdriver import Chrome
from selenium import webdriver


loop = asyncio.get_event_loop()
proxy_list = []


def get_proxies():
    proxies = requests.get("https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt")
    proxies = proxies.text.split("\n")[9:]
    proxies = [p.split(" ")[0] for p in proxies]
    return proxies


def visit_site(web_url,driver=None):
    if driver:
        driver.close()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % random.choice(proxy_list))
    driver = Chrome("./chromedriver.exe", options=chrome_options)
    driver.get(web_url)
    loop.call_later(1, visit_site, web_url,driver)


if __name__ == "__main__":
    proxy_list = get_proxies()
    visit_site("https://blog.botfun.ir")
    loop.run_forever()
