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

def safe_click(driver, xpath,tick=5):
    i=0
    while True:
        try:
            i+=1
            time.sleep(1)
            button = driver.find_element_by_xpath(xpath)
            button.click()
            return True
        except Exception:
            if(i>tick):
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
    url = 'http://hrss.hlj.gov.cn/hrss/'

    driver.get(url)

    # 输入框
    input = safe_get_element_by_xpath(driver, './/div[@class="search"]//input')
    input.send_keys("大学生就业")

    # 搜索按钮
    safe_click(driver, './/button[@role="button"]')
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    href_arrays = set()
    limit = 600

    while True:
        href_elements = safe_get_elements(driver, './/div[@class="list-title  clearfix"]/a')
        for ele in href_elements:
            href_arrays.add(ele.get_attribute('href'))

        if len(href_arrays) > limit:
            break

        print(len(href_arrays))

        time.sleep(3)
        has_next = safe_click(driver, './/li[@class="next"]/a')
        if has_next:
            continue
        else:
            break

    print(len(href_arrays))
    with open('../Policy/txt/HeiLongJiangPolicy.txt', 'w') as f:
        for ele in href_arrays:
            f.write(str(ele) + '\n')


# 初始化csv
def initCsv():
    with open('../Policy/csv/黑龙江.csv', 'a', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["时间", "网站", "内容", "来源",])


def getHtml():
    with open('../Policy/txt/HeiLongJiangPolicy.txt', 'r') as f:
        hrefs = [line.strip() for line in f]

    for url in hrefs:
        try:
            driver.get(url)
        except Exception:
            continue
        # 获取时间
        time_element = safe_get_element_by_xpath(driver, './/span[@class="date"]/b')
        if not time_element:
            pub_time = ""
        else:
            pub_time = time_element.text
            match1 = re.search(r'\d{4}-\d{2}-\d{2}', pub_time)
            if match1:
                pub_time = match1.group()
                print('match1',pub_time)

        print(pub_time)


        # 获取来源
        source_element = safe_get_element_by_xpath(driver,'.//span[@class="ly"]/b')
        if not source_element:
            source="黑龙江省人力资源和社会保障厅"
        else:
            source=source_element.text

        #获取内容
        text_parent=safe_get_element_by_id(driver,'zoomcon')
        if not text_parent:
            texts=""
        else:
            texts_element = text_parent.find_elements_by_xpath('.//*')
            texts = ""
            for item in texts_element:
                texts += str(item.text)
            texts = texts.replace('\n', '.').replace('\r', '.')
            texts = texts.replace('\t', '.')
        if "大学生" not in texts and "毕业生" not in texts and "高校" not in texts and '校园' not in texts:
            continue
        print(texts)
        with open('../Policy/csv/黑龙江.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(pub_time)] + [str(driver.current_url)] + [str(texts)] + [str(source)])


if __name__ == '__main__':
    initCsv()
    #getUrls()
    getHtml()
