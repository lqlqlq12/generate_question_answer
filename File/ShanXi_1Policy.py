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
    # 资讯
    url = 'http://rst.shanxi.gov.cn/dept_search/#/News?keywords=%E5%A4%A7%E5%AD%A6%E7%94%9F%E5%B0%B1%E4%B8%9A&siteTag=1&siteid=25'
    driver.get(url)

    href_arrays = set()
    limit = 12000

    while True:
        href_elements = safe_get_elements(driver, './/div[@class="news"]//div[@class="table_9"]/div/a')
        for ele in href_elements:
            print(ele.get_attribute('href'))
            href_arrays.add(ele.get_attribute('href'))

        if len(href_arrays) > limit:
            break

        print(len(href_arrays))

        time.sleep(1)
        has_next = safe_click(driver, './/div[@class="el-pagination"]//button[@class="btn-next"]')
        next_button = safe_get_element_by_xpath(driver, './/button[@disabled="disabled"]')
        if next_button:
            break
        if has_next:
            continue
        else:
            break

    with open('../Policy/txt/ShanXi_1Policy.txt', 'w') as f:
        for ele in href_arrays:
            f.write(str(ele) + '\n')


# 初始化csv
def initCsv():
    with open('../Policy/csv/山西.csv', 'a', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["时间", "网站", "内容", "来源", ])


def getHtml():
    with open('../Policy/txt/ShanXi_1Policy.txt', 'r') as f:
        hrefs = [line.strip() for line in f]

    for url in hrefs:
        try:
            driver.get(url)
        except Exception:
            continue

        # 获取内容
        text_parent = safe_get_element_by_xpath(driver, './/div[@class="TRS_Editor"]')
        if not text_parent:
            texts = ""
        else:
            texts_element = text_parent.find_elements_by_xpath('.//*')
            texts = ""
            for item in texts_element:
                texts += str(item.text)
            texts = texts.replace('\n', '.').replace('\r', '.').replace('\t', '.')

        if "大学生" not in texts and "毕业生" not in texts:
            continue
        print(texts)


        # 获取时间
        time_element = safe_get_element_by_xpath(driver, './/p[@class="box_p"]/span[1]')
        if not time_element:
            pub_time = ""
        else:
            pub_time = time_element.text
            match = re.search(r'\d{4}-\d{2}-\d{2}', pub_time)
            if match:
                pub_time = match.group()
        print(pub_time)

        source = ""
        # 获取来源
        source_element = safe_get_element_by_xpath(driver, './/p[@class="box_p"]/span[3]')
        if not source_element:
            source = "山西省人力资源和社会保障厅"
        else:
            source = source_element.text
            source = str(source).split('：')[1].strip()
        print(source)

        with open('../Policy/csv/山西.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(pub_time)] + [str(driver.current_url)] + [str(texts)] + [str(source)])

        print('write in',driver.current_url)


if __name__ == '__main__':
    # getUrls()
    initCsv()
    getHtml()
