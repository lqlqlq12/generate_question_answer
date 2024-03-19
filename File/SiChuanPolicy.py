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
    url = 'http://rst.sc.gov.cn/rst/jycygzdt/zlList.shtml'

    driver.get(url)

    href_arrays = set()
    limit = 12000

    i = 0
    while True:
        pre = len(href_arrays)
        href_elements = safe_get_elements(driver, './/ul[@class="man-top20"]/li/a')
        for ele in href_elements:
            print(ele.get_attribute('href'))
            href_arrays.add(ele.get_attribute('href'))
        if pre == len(href_arrays):
            break
        if len(href_arrays) > limit:
            break

        print(len(href_arrays))
        has_next = safe_click(driver, './/div[@class="pagination_index"][last()]')
        if has_next:
            continue
        else:
            break

    url = 'http://rst.sc.gov.cn/guestweb4/s?searchWord=%25E6%25AF%2595%25E4%25B8%259A%25E7%2594%259F%25E5%25B0%25B1%25E4%25B8%259A&column=%25E5%2585%25A8%25E9%2583%25A8&wordPlace=0&orderBy=0&startTime=&endTime=&pageSize=10&pageNum=0&timeStamp=0&siteCode=5100000042&siteCodes=&checkHandle=1&strFileType=%25E5%2585%25A8%25E9%2583%25A8%25E6%25A0%25BC%25E5%25BC%258F&sonSiteCode=&areaSearchFlag=1&secondSearchWords=&countKey=%200&left_right_index=0'
    driver.get(url)
    while True:
        href_elements = safe_get_elements(driver, './/div[@class="bigTit clearfix"]/a')
        for ele in href_elements:
            print(ele.get_attribute('href'))
            href_arrays.add(ele.get_attribute('href'))

        if len(href_arrays) > limit:
            break

        print(len(href_arrays))
        has_next = safe_click(driver, './/li[@class="next"]')
        if has_next:
            continue
        else:
            break

    with open('../Policy/txt/SiChuanPolicy.txt', 'w') as f:
        for ele in href_arrays:
            f.write(str(ele) + '\n')


# 初始化csv
def initCsv():
    with open('../Policy/csv/四川.csv', 'a', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["时间", "网站", "内容", "来源", "浏览次数"])


def getHtml():
    with open('../Policy/txt/SiChuanPolicy.txt', 'r') as f:
        hrefs = [line.strip() for line in f]

    for url in hrefs:
        try:
            driver.get(url)
        except Exception:
            continue
        # 获取内容
        texts = ""
        text_parent = safe_get_element_by_xpath(driver, './/div[@id="print"]')
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
        time_element = safe_get_element_by_xpath(driver, './/span[@id="publishedTime"]')
        if not time_element:
            pub_time = ""
        else:
            pub_time = time_element.text
            match = re.search(r'\d{4}-\d{2}-\d{2}', pub_time)
            if match:
                pub_time = match.group()

        print(pub_time)

        # 获取来源
        source_element = safe_get_element_by_xpath(driver, './/table/tbody/tr/td[2]/span')
        if not source_element:
            source = ""
        else:
            source = source_element.text
        print(source)

        # 点击次数
        reader_element = safe_get_element_by_xpath(driver, './/table/tbody/tr/td[3]/span')
        if reader_element:
            reader = reader_element.text
            readers = str(reader).split('次')[0]
        else:
            readers = 0
        print(readers)

        with open('../Policy/csv/四川.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(pub_time)] + [str(driver.current_url)] + [str(texts)] + [str(source)] + [str(readers)])
        print('write in', driver.current_url)


if __name__ == '__main__':
    # getUrls()
    initCsv()
    getHtml()
