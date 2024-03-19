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
    #工作开展
    url = 'https://rst.ln.gov.cn/rst/ztzl/jycyzc/gzkz/index.shtml'
    driver.get(url)

    href_arrays = set()
    limit = 600

    head_url='https://rst.ln.gov.cn'

    while True:
        href_elements = safe_get_elements(driver, './/li/a[@class="inpageContentListText"]')
        for ele in href_elements:
            print(ele.get_attribute('href'))
            href_arrays.add(ele.get_attribute('href'))

        if len(href_arrays) > limit:
            break

        print(len(href_arrays))

        time.sleep(3)
        has_next = safe_click(driver, './/a[@title="下一页"]')
        if has_next:
            continue
        else:
            break

    #政策解读
    url="https://rst.ln.gov.cn/rst/ztzl/jycyzc/zcjd/index.shtml"
    driver.get(url)
    while True:
        href_elements = safe_get_elements(driver, './/li/a[@class="inpageContentListText"]')
        for ele in href_elements:
            print(ele.get_attribute('href'))
            href_arrays.add(ele.get_attribute('href'))


        if len(href_arrays) > limit:
            break

        print(len(href_arrays))

        time.sleep(3)
        has_next = safe_click(driver, './/a[@title="下一页"]')
        if has_next:
            continue
        else:
            break
    print(len(href_arrays))

    with open('../Policy/txt/LiaoNingPolicy.txt', 'w') as f:
        for ele in href_arrays:
            f.write(str(ele) + '\n')


# 初始化csv
def initCsv():
    with open('../Policy/csv/辽宁.csv', 'a', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["时间", "网站", "内容", "来源"])


def getHtml():
    with open('../Policy/txt/LiaoNingPolicy.txt', 'r') as f:
        hrefs = [line.strip() for line in f]

    for url in hrefs:
        try:
            driver.get(url)
        except Exception:
            continue
        # 获取时间
        time_element = safe_get_element_by_xpath(driver, './/div[@class="contentSource"]/p[3]')
        if not time_element:
            pub_time = ""
        else:
            pub_time = time_element.text
            pub_time=str(pub_time).split('：')[1].strip()
            date_object = datetime.strptime(pub_time, "%Y年%m月%d日")
            pub_time = date_object.strftime("%Y-%m-%d")
        print(pub_time)


        # 获取来源
        source_element = safe_get_element_by_xpath(driver,'.//div[@class="contentSource"]/p[2]')
        if not source_element:
            source="辽宁省人力资源和社会保障厅"
        else:
            source=source_element.text
            source=str(source).split('：')[1].strip()

        #获取内容
        text_parent=safe_get_element_by_xpath(driver,'.//div[@class="inpageContentText"]')
        if not text_parent:
            texts=""
        else:
            texts_element = text_parent.find_elements_by_xpath('.//*')
            texts = ""
            for item in texts_element:
                texts += str(item.text)
            texts = texts.replace('\n', '.').replace('\r', '.').replace('\t', '.')

        if "大学生" not in texts and "毕业生" not in texts and "高校" not in texts:
            continue
        print(texts)
        with open('../Policy/csv/辽宁.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(pub_time)] + [str(driver.current_url)] + [str(texts)] + [str(source)])
        print('write in',driver.current_url)


if __name__ == '__main__':
    #getUrls()
    initCsv()
    getHtml()
