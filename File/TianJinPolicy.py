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


def getHrefs(driver, href_arrays):
    href_elements = safe_get_elements(driver, './/tr[@class="data_line"]//a')
    for ele in href_elements:
        print(ele.get_attribute('href'))
        href_arrays.add(ele.get_attribute('href'))
    print(len(href_arrays))
    time.sleep(3)


def getUrls():
    href_arrays = set()
    limit = 12000

    # 大学生就业
    url = 'http://publicservices.hrss.tj.gov.cn/ecdomain/framework/zcydt/fbbafimfopkibboikmfajfanojgaanpa.jsp?term=410'
    driver.get(url)

    getHrefs(driver, href_arrays)

    # 大学生就业见习
    url = 'http://publicservices.hrss.tj.gov.cn/ecdomain/framework/zcydt/fbbafimfopkibboikmfajfanojgaanpa.jsp?term=409'
    driver.get(url)
    getHrefs(driver, href_arrays)

    # 大学生三支一扶计划
    url = 'http://publicservices.hrss.tj.gov.cn/ecdomain/framework/zcydt/fbbafimfopkibboikmfajfanojgaanpa.jsp?term=410'
    driver.get(url)
    getHrefs(driver, href_arrays)

    # 大学生创业
    url = 'http://publicservices.hrss.tj.gov.cn/ecdomain/framework/zcydt/fbbafimfopkibboikmfajfanojgaanpa.jsp?term=444'
    driver.get(url)
    getHrefs(driver, href_arrays)

    # 创业担保贷款
    url = 'http://publicservices.hrss.tj.gov.cn/ecdomain/framework/zcydt/fbbafimfopkibboikmfajfanojgaanpa.jsp?term=446'
    driver.get(url)
    getHrefs(driver, href_arrays)

    # 政策文件
    url = 'http://publicservices.hrss.tj.gov.cn/ecdomain/framework/zcydt/fbbafimfopkibboikmfajfanojgaanpa.jsp?term=536'
    driver.get(url)
    getHrefs(driver, href_arrays)
    # 政策文件第二页
    url = 'http://publicservices.hrss.tj.gov.cn/ecdomain/framework/zcydt/fbbafimfopkibboikmfajfanojgaanpa.jsp?term=536'
    driver.get(url)
    getHrefs(driver, href_arrays)

    with open('../Policy/TianJinPolicy_1.txt', 'w') as f:
        for ele in href_arrays:
            f.write(str(ele) + '\n')

    href_arrays.clear()

    url = 'https://hrss.tj.gov.cn/searchsite/tjsrlzyhshbzj_215/search.html?siteId=56&searchWord=%E5%A4%A7%E5%AD%A6%E7%94%9F%E5%B0%B1%E4%B8%9A'
    driver.get(url)

    while True:
        href_elements = safe_get_elements(driver, './/div[@class="tit"]/a')
        for ele in href_elements:
            print(ele.get_attribute('href'))
            href_arrays.add(ele.get_attribute('href'))

        if len(href_arrays) > limit:
            break

        print(len(href_arrays))

        time.sleep(3)
        pre = driver.current_url
        has_next = safe_click(driver, './/a[@ng-click="selectNext()"]')
        # 点下一页没有跳转
        if pre == driver.current_url:
            break
        if has_next:
            continue
        else:
            break

    with open('../Policy/txt/TianJinPolicy_2.txt', 'w') as f:
        for ele in href_arrays:
            f.write(str(ele) + '\n')


# 初始化csv
def initCsv():
    with open('../Policy/csv/天津.csv', 'a', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["时间", "网站", "内容", "来源", ])


def getHtml():
    with open('../Policy/txt/TianJinPolicy_1.txt', 'r') as f:
        hrefs = [line.strip() for line in f]

    for url in hrefs:
        driver.get(url)
        if "404" in driver.title:
            print(404)
            continue

        pub_time = ""

        # 获取来源
        source_element = safe_get_element_by_xpath(driver, './/div[@class="Nei_news_blueone0"]')
        if not source_element:
            source = "天津市人力资源和社会保障局"
        else:
            source = source_element.text
            source = str(source).split('：')[1].strip()
        print(source)

        # 获取内容
        text_parent = safe_get_element_by_id(driver, "newscontent")
        if not text_parent:
            texts = ""
        else:
            texts_element = text_parent.find_elements_by_xpath('.//*')
            texts = ""
            for item in texts_element:
                texts += str(item.text)
            texts = texts.replace('\n', '.').replace('\r', '.').replace('\t', '.')
        if "大学生" not in texts and "毕业生" not in texts and "高校" not in texts:
            continue
        print(texts)
        with open('../Policy/csv/天津.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(pub_time)] + [str(driver.current_url)] + [str(texts)] + [str(source)])
        print('write in')

    with open('../Policy/txt/TianJinPolicy_2.txt', 'r') as f:
        hrefs = [line.strip() for line in f]

    for url in hrefs:
        driver.get(url)

        pub_time = ""
        time_element = safe_get_element_by_xpath(driver, './/div[@class="article-line-2 fl"]')
        if time_element:
            match = re.search(r'\d{4}-\d{2}-\d{2}', str(time_element.text))
            if match:
                pub_time = match.group()
        print(pub_time)

        # 获取来源
        source_element = safe_get_element_by_xpath(driver, './/div[@class="article-line-1 fl"]')
        if not source_element:
            source = "天津市人力资源和社会保障局"
        else:
            source = source_element.text
            source = str(source).split('：')[1].strip()
        print(source)

        # 获取内容
        text_parent = safe_get_element_by_id(driver, "zoom")
        if not text_parent:
            texts = ""
        else:
            texts_element = text_parent.find_elements_by_xpath('.//*')
            texts = ""
            for item in texts_element:
                texts += str(item.text)
            texts = texts.replace('\n', '.').replace('\r', '.').replace('\t', '.')
        if "大学生" not in texts and "毕业生" not in texts and "高校" not in texts:
            continue
        print(texts)
        with open('../Policy/csv/天津.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(pub_time)] + [str(driver.current_url)] + [str(texts)] + [str(source)])
        print('write in', driver.current_url)


if __name__ == '__main__':
    # getUrls()
    initCsv()
    getHtml()
