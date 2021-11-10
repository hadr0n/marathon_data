import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import datetime
import re
import json
import time
import pandas as pd
import mechanize
import http.cookiejar, urllib.request
from textwrap import dedent



def make_soup_sel(url, browser):
    browser.get(url)
    html_source = browser.execute_script("return document.documentElement.outerHTML;").encode("utf-8")
    soup = BeautifulSoup(html_source).body
    return soup


def make_soup_mech(url, browser):
    soup = BeautifulSoup(browser.open(url).read())
    return soup

main_link = 'https://chicago-history.r.mikatiming.com/2019/?lang=EN_CAP'
