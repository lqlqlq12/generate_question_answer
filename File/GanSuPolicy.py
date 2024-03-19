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
    url='http://rst.gansu.gov.cn/guestweb4/s?siteCode=6200000051&checkHandle=1&pageSize=10&left_right_index=0&searchWord=%E6%AF%95%E4%B8%9A%E7%94%9F%E5%B0%B1%E4%B8%9A'

    driver.get(url)

    href_arrays = set()
    limit = 12000

    while True:
        href_elements = safe_get_elements(driver, './/div[@class="bigTit clearfix"]/a')
        for ele in href_elements:
            print(ele.get_attribute('href'))
            href_arrays.add(ele.get_attribute('href'))

        if len(href_arrays) > limit:
            break

        print(len(href_arrays))
        has_next = safe_click(driver, './/ul[@id="pageInfo"]/li[last()]')
        tile=safe_get_element_by_xpath(driver,'.//ul[@id="pageInfo"]/li[last()]')
        if tile.get_attribute('class')=="next disabled":
            break
        if has_next:
            continue
        else:
            break

    with open('../Policy/txt/GanSuPolicy.txt', 'w') as f:
        for ele in href_arrays:
            f.write(str(ele) + '\n')


# 初始化csv
def initCsv():
    with open('../Policy/csv/甘肃.csv', 'a', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["时间", "网站", "内容", "来源","浏览次数"])


def getHtml():
    with open('../Policy/txt/GanSuPolicy.txt', 'r') as f:
        hrefs = [line.strip() for line in f]

    for url in hrefs:
        try:
            driver.get(url)
        except Exception:
            continue
        # 获取内容
        texts=""
        text_parent = safe_get_element_by_xpath(driver, './/div[@class="letterdetail"]')
        if not text_parent:
            text_parent=safe_get_element_by_xpath(driver,'.//div[@class="newsdetail"]')
            print('find')
        if text_parent:
            texts_element = text_parent.find_elements_by_xpath('.//*')
            texts = ""
            for item in texts_element:
                texts += str(item.text)
            texts = texts.replace('\n', '.').replace('\r', '.')
            texts = texts.replace('\t', '.').replace('\r', '.')

        if "大学生" not in texts and "毕业生" not in texts and "高校" not in texts:
            continue
        print(texts)

        # 获取时间
        time_element = safe_get_element_by_xpath(driver, './/div[@class="new-time"]/span')
        if not time_element:
            pub_time = ""
        else:
            pub_time = time_element.text
            match = re.search(r'\d{4}-\d{2}-\d{2}', pub_time)
            if match:
                pub_time = match.group()

        print(pub_time)

        # 获取来源
        source="甘肃省人力资源和社会保障厅"

        #点击次数
        reader_element=safe_get_element_by_xpath(driver,'.//i[@id="doc_span_id"]')
        if reader_element:
            readers=reader_element.text
        else:
            readers=0
        print(readers)


        with open('../Policy/csv/甘肃.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(pub_time)] + [str(driver.current_url)] + [str(texts)] + [str(source)]+[str(readers)])
        print('write in', driver.current_url)


if __name__ == '__main__':
    # getUrls()
    initCsv()
    getHtml()
