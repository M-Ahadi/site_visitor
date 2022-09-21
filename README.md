# Site Visitor

A simple code that uses different proxies to increase a website traffic.

In order to use it, it is required to config these variables:

```
SITE_VISIT_PERIOD=1 				  # time to wait for next visit in seconds
URLS=https://m-ahadi.ir,https://blog.m-ahadi.ir   # Website urls you want to increase its traffic 
USE_PROXY=True 					  # use proxy to visit website from different countries
LOG_LEVEL=info					  # display log, options: debug,info, warning, error, critical
PARALLELS=3 					  # number of parallel website visit
MINIMUM_VISIT=60 				  # minimum time to visit a page in second
MAXIMUM_VISIT=100 				  # maximum time to visit a page in second
```


To run the code in windows download chromedriver for windows from url blow:

https://chromedriver.chromium.org/downloads
