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
    url='https://rlsbj.cq.gov.cn/cqs/searchResultPC.html?tenantId=82&configTenantId=82&areaCode=500000121&searchWord=%E6%AF%95%E4%B8%9A%E7%94%9F%E5%B0%B1%E4%B8%9A&dataTypeId=1861&dataTypeName=%E6%94%BF%E5%8A%A1%E4%BF%A1%E6%81%AF&pageSize=10&seniorBox=0&advancedFilters=&isAdvancedSearch=0&searchBy=all'

    driver.get(url)

    href_arrays = set()
    limit = 12000

    while True:
        href_elements = safe_get_elements(driver, './/div[@class="item is-news"]//a')
        for ele in href_elements:
            print(ele.get_attribute('href'))
            href_arrays.add(ele.get_attribute('href'))

        if len(href_arrays) > limit:
            break

        print(len(href_arrays))
        has_next = safe_click(driver, './/a[@class="layui-laypage-next"]')
        if has_next:
            continue
        else:
            break



    url='https://rlsbj.cq.gov.cn/cqs/searchResultPC.html?tenantId=82&configTenantId=82&areaCode=500000121&searchWord=%E6%AF%95%E4%B8%9A%E7%94%9F%E5%B0%B1%E4%B8%9A&dataTypeId=1961&dataTypeName=%E6%94%BF%E7%AD%96%E6%96%87%E4%BB%B6&pageSize=10&seniorBox=0&advancedFilters=&isAdvancedSearch=0&searchBy=all'
    driver.get(url)
    while True:
        href_elements = safe_get_elements(driver, './/div[@class="title"]//a')
        for ele in href_elements:
            print(ele.get_attribute('href'))
            href_arrays.add(ele.get_attribute('href'))

        if len(href_arrays) > limit:
            break

        print(len(href_arrays))
        has_next = safe_click(driver, './/a[@class="layui-laypage-next"]')
        if has_next:
            continue
        else:
            break

    with open('../Policy/txt/ChongQingPolicy.txt', 'w') as f:
        for ele in href_arrays:
            f.write(str(ele) + '\n')


# 初始化csv
def initCsv():
    with open('../Policy/csv/重庆.csv', 'a', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["时间", "网站", "内容", "来源"])


def getHtml():
    with open('../Policy/txt/ChongQingPolicy.txt', 'r') as f:
        hrefs = [line.strip() for line in f]

    for url in hrefs:
        try:
            driver.get(url)
        except Exception:
            continue
        print(url)
        # 获取内容
        texts=""
        text_parent = safe_get_element_by_xpath(driver, './/div[@class="zwxl-article"]')
        if not text_parent:
            text_parent=safe_get_element_by_xpath(driver,'.//div[@class="zcwjk-xlcon"]')
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
        time_element = safe_get_element_by_xpath(driver, './/span[@class="con"][1]')
        if not time_element:
            time_element=safe_get_element_by_xpath(driver,'.//table/tbody/tr[4]/td[4]')
        if not time_element:
            pub_time = ""
        else:
            pub_time = time_element.text
            match = re.search(r'\d{4}-\d{2}-\d{2}', pub_time)
            if match:
                pub_time = match.group()

        print(pub_time)

        # 获取来源
        source_element=safe_get_element_by_xpath(driver,'.//span[@class="con"][2]')
        if not source_element:
            source_element=safe_get_element_by_xpath(driver,'.//table/tbody/tr[3]/td[2]')
            if not source_element:
                source="重庆市人力资源和社会保障局"
        if source_element:
            source=source_element.text
        print(source)

        with open('../Policy/csv/重庆.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(pub_time)] + [str(driver.current_url)] + [str(texts)] + [str(source)])
        print('write in')


if __name__ == '__main__':
    # getUrls()
    initCsv()
    getHtml()
