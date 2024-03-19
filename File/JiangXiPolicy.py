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
    url = 'http://sousuo.jiangxi.gov.cn/jsearchfront/search.do?websiteid=360000000234000&tpl=301&q=%E6%AF%95%E4%B8%9A%E7%94%9F%E5%B0%B1%E4%B8%9A&p=1&pg=&pos=&searchid=841&oq=&eq=&begin=&end='
    driver.get(url)

    href_arrays = set()
    limit = 12000

    while True:
        has_next = safe_click(driver, './/div[@class="uploadmore"]')
        if has_next:
            try:
                tile = has_next.get_attribute('style')
                if tile == "display: none;":
                    break
            except Exception:
                continue
        else:
            break

    href_elements = safe_get_elements(driver, './/div[@class="jcse-news-title"]/a')
    for ele in href_elements:
        print(ele.get_attribute('href'))
        href_arrays.add(ele.get_attribute('href'))

    print(len(href_arrays))

    with open('../Policy/txt/JiangXiPolicy.txt', 'w') as f:
        for ele in href_arrays:
            f.write(str(ele) + '\n')


# 初始化csv
def initCsv():
    with open('../Policy/csv/江西.csv', 'a', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["时间", "网站", "内容", "来源","浏览次数"])


def getHtml():
    with open('../Policy/txt/JiangXiPolicy.txt', 'r') as f:
        hrefs = [line.strip() for line in f]

    for url in hrefs:
        try:
            driver.get(url)
        except:
            continue
        # 获取内容
        text_parent = safe_get_element_by_xpath(driver, './/div[@class="main-wrapper"]')
        if not text_parent:
            texts = ""
        else:
            texts_element = text_parent.find_elements_by_xpath('.//*')
            texts = ""
            for item in texts_element:
                texts += str(item.text)
            texts = re.sub('([^\u4e00-\u9fa5\u0030-\u0039])', '', texts)

        if "大学生" not in texts and "毕业生" not in texts and "高校" not in texts:
            continue
        print(texts)

        # 获取时间
        time_element = safe_get_element_by_xpath(driver, './/div[@class="post_time_source"]/span[2]')
        if not time_element:
            pub_time = ""
        else:
            pub_time = time_element.text
            match = re.search(r'\d{4}-\d{2}-\d{2}', pub_time)
            if match:
                pub_time = match.group()
        print(pub_time)

        # 获取来源
        source_element = safe_get_element_by_xpath(driver, './/div[@class="post_time_source"]/span[1]')
        if not source_element:
            source = ""
        else:
            source = source_element.text
            source = str(source).split("：")[1]
        print(source)

        # 获取浏览次数
        reader_element = safe_get_element_by_xpath(driver, './/div[@class="post_time_source"]/span[3]/span')
        if not reader_element:
            readers = 0
        else:
            try:
                readers = reader_element.text
            except Exception:
                readers = 0
        print(readers)

        with open('../Policy/csv/江西.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(pub_time)] + [str(driver.current_url)] + [str(texts)] + [str(source)]+[str(readers)])
        print('write in', driver.current_url)


if __name__ == '__main__':
    #getUrls()
    initCsv()
    getHtml()
