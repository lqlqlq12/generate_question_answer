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
    url = 'http://search.gd.gov.cn/search/all/186?keywords=%E6%AF%95%E4%B8%9A%E7%94%9F%E5%B0%B1%E4%B8%9A'
    driver.get(url)

    href_arrays = set()
    limit = 12000

    i = 1
    while True:
        pre = len(href_arrays)
        href_elements = safe_get_elements(driver, './/div[@class="list-body"]/div/a[1]')
        for ele in href_elements:
            print(ele.get_attribute('href'))
            href_arrays.add(ele.get_attribute('href'))
        if pre == len(href_arrays):
            break
        if len(href_arrays) > limit:
            break

        print(len(href_arrays))
        i += 1
        url = f"http://search.gd.gov.cn/search/all/186?page=%d"%(i)+"&keywords=%E6%AF%95%E4%B8%9A%E7%94%9F%E5%B0%B1%E4%B8%9A"
        try:
            driver.get(url)
        except Exception:
            break

    with open('../Policy/txt/GuangDongPolicy.txt', 'w') as f:
        for ele in href_arrays:
            f.write(str(ele) + '\n')


# 初始化csv
def initCsv():
    with open('../Policy/csv/广东.csv', 'a', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["时间", "网站", "内容", "来源"])


def getHtml():
    with open('../Policy/txt/GuangDongPolicy.txt', 'r') as f:
        hrefs = [line.strip() for line in f]

    for url in hrefs:
        try:
            driver.get(url)
        except Exception:
            continue
        # 获取内容
        texts = ""
        text_parent = safe_get_element_by_xpath(driver, './/div[@class="article"]')
        if text_parent:
            texts_element = text_parent.find_elements_by_xpath('.//*')
            texts = ""
            for item in texts_element:
                texts += str(item.text)
            texts = texts.replace('\n', '.').replace('\r', '.')
            texts = texts.replace('\t', '.').replace('\r', '.')

        if "大学生" not in texts and "毕业生" not in texts and "高校" not in texts and '校园' not in texts:
            continue
        print(texts)

        # 获取时间
        time_element = safe_get_element_by_xpath(driver, './/span[@class="article_item_tem"][2]')
        if not time_element:
            pub_time = ""
        else:
            pub_time = time_element.text
            match = re.search(r'\d{4}-\d{2}-\d{2}', pub_time)
            if match:
                pub_time = match.group()

        print(pub_time)

        # 获取来源
        source_element = safe_get_element_by_xpath(driver, './/span[@class="article_item_tem"][1]')
        if not source_element:
            source = ""
        else:
            source = source_element.text
            source=str(source).split('：')[1]
        if source=="本网":
            source="广东省人力资源和社会保障厅"
        print(source)


        with open('../Policy/csv/广东.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(pub_time)] + [str(driver.current_url)] + [str(texts)] + [str(source)])
        print('write in', driver.current_url)


if __name__ == '__main__':
    # getUrls()
    initCsv()
    getHtml()
