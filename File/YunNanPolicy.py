import json

import certifi
import requests
import urllib3
from bs4 import BeautifulSoup
import time
from datetime import datetime
import re
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import xlwt
import csv
from msedge.selenium_tools import EdgeOptions
from requests_html import HTMLSession

driver = webdriver.Firefox(executable_path='D:\software\FireFoxDriver\geckodriver.exe')


def safe_click(driver, xpath, tick=5):
    i = 0
    while True:
        try:
            i += 1
            time.sleep(1)
            button = driver.find_element_by_xpath(xpath)
            button.click()
            return True
        except Exception:
            if (i > tick):
                return False


def safe_get_element_by_xpath(driver, xpath, tick=3):
    i = 0
    while True:
        try:
            i += 1
            time.sleep(1)
            element = driver.find_element_by_xpath(xpath)
            return element
        except Exception:
            if (i > tick):
                break
            continue


def safe_get_elements(driver, xpath, tick=3):
    i = 0
    while True:
        try:
            i += 1
            time.sleep(1)
            elements = driver.find_elements_by_xpath(xpath)
            return elements
        except Exception:
            if (i > tick):
                break
            continue


def safe_get_element_by_id(driver, id, tick=3):
    i = 0
    while True:
        try:
            i += 1
            time.sleep(1)
            element = driver.find_element_by_id(id)
            return element
        except Exception:
            if (i > tick):
                break
            continue


def getUrls():
    url = 'http://hrss.yn.gov.cn/SearchList.aspx?kw=%E6%AF%95%E4%B8%9A%E7%94%9F%E5%B0%B1%E4%B8%9A'

    driver.get(url)

    href_arrays = set()
    limit = 12000

    i = 2
    while True:
        href_elements = safe_get_elements(driver, './/ul[@class="ul13 pd20"]/li/a')
        for ele in href_elements:
            print(ele.get_attribute('href'))
            href_arrays.add(ele.get_attribute('href'))
        if len(href_arrays) > limit:
            break
        print(len(href_arrays))
        has_next = safe_click(driver, './/a[@href="/SearchList.aspx?kw=毕业生就业&page=%d&Cid="]' % (i))
        i += 1
        if has_next:
            continue
        else:
            break

    with open('../Policy/txt/YunNanPolicy.txt', 'w') as f:
        for ele in href_arrays:
            f.write(str(ele) + '\n')


# 初始化csv
def initCsv():
    with open('../Policy/csv/云南.csv', 'a', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["时间", "网站", "内容", "来源", "浏览次数"])


def getHtml():
    with open('../Policy/txt/YunNanPolicy.txt', 'r') as f:
        hrefs = [line.strip() for line in f]

    for url in hrefs:
        try:
            driver.get(url)
        except Exception:
            continue
        # 获取内容
        texts = ""
        text_parent = safe_get_element_by_xpath(driver, './/span[@id="Body_ltl_newsContent"]')
        if text_parent:
            texts_element = text_parent.find_elements_by_xpath('.//*')
            texts = ""
            for item in texts_element:
                texts += str(item.text)
            texts = texts.replace('\n', '.').replace('\r', '.').replace('\t', '.')

        if "大学生" not in texts and "毕业生" not in texts and "高校" not in texts and '校园' not in texts:
            continue
        print(texts)

        # 获取时间
        time_element = safe_get_element_by_xpath(driver, './/span[@id="Body_lb_postTime"]')
        if not time_element:
            pub_time = ""
        else:
            pub_time = time_element.text
            match = re.search(r'\d{4}/\d{2}/\d{2}', pub_time)
            if not match:
                match = re.search(r'\d{4}/\d{1}/\d{2}', pub_time)
            if not match:
                match = re.search(r'\d{4}/\d{1}/\d{1}', pub_time)
            if not match:
                match = re.search(r'\d{4}/\d{2}/\d{1}', pub_time)
            if match:
                pub_time = match.group()
                pub_time = pub_time.replace('/', '-')

        print(pub_time)

        # 获取来源
        source_element = safe_get_element_by_xpath(driver, './/span[@id="Body_lb_NewsOrigin"]')
        if not source_element:
            source = "云南人力资源和社会保障网"
        else:
            try:
                source = str(source_element.text)
            except Exception:
                source = "云南人力资源和社会保障网"
        print(source)

        # 获取点击数
        readers_element = safe_get_element_by_xpath(driver, 'id="Body_lb_newsclick"')
        if readers_element:
            readers = readers_element.text
        else:
            readers = 0

        with open('../Policy/csv/云南.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(pub_time)] + [str(driver.current_url)] + [str(texts)] + [str(source)] + [str(readers)])
        print('write in', driver.current_url)


if __name__ == '__main__':
    # getUrls()
    initCsv()
    getHtml()
