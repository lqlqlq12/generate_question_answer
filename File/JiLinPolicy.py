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
    url = 'http://www.jlhr.com.cn/col/zhengce/index.html'
    driver.get(url)

    href_arrays = set()
    limit = 600

    # 省级按钮
    result = safe_click(driver, './/ul[@id="nav"]/li[2]')
    if result:
        while True:
            href_elements = safe_get_elements(driver, './/li[@style="display: block;"]//div[@class="m_d"]/a')
            for ele in href_elements:
                href_arrays.add(ele.get_attribute('href'))

            if len(href_arrays) > limit:
                break

            print(len(href_arrays))

            time.sleep(3)
            has_next = safe_click(driver, './/li[@style="display: block;"]//a[@class="next"]')
            if has_next:
                continue
            else:
                break

        print(len(href_arrays))

    # 市县按钮
    result = safe_click(driver, './/ul[@id="nav"]/li[3]')
    if result:
        while True:
            href_elements = safe_get_elements(driver, './/li[@style="display: block;"]//div[@class="m_d"]/a')
            for ele in href_elements:
                href_arrays.add(ele.get_attribute('href'))

            if len(href_arrays) > limit:
                break

            print(len(href_arrays))

            time.sleep(3)
            has_next = safe_click(driver, './/li[@style="display: block;"]//a[@class="next"]')
            if has_next:
                continue
            else:
                break

        print(len(href_arrays))

    with open('../Policy/txt/JiLinPolicy.txt', 'w') as f:
        for ele in href_arrays:
            f.write(str(ele) + '\n')


# 初始化csv
def initCsv():
    with open('../Policy/csv/吉林.csv', 'a', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["时间", "网站", "内容", "来源", "浏览量"])


def getHtml():
    with open('../Policy/txt/JiLinPolicy.txt', 'r') as f:
        hrefs = [line.strip() for line in f]

    for url in hrefs:
        driver.get(url)

        #获取时间、来源、浏览量
        msg=safe_get_element_by_xpath(driver,'.//div[@class="art-date"]')
        pub_time = ""
        source = ""
        reader=0
        if msg:
            '发布时间：2016-03-21 来源：吉林省人才交流开发中心： 浏览次数：'
            parts=str(msg.text).split()
            pub_time=parts[0].split('：')[1]
            source=parts[1].split('：')[1]
            readers_element=safe_get_element_by_id(driver,'llcs')
            if readers_element:
                reader=readers_element.text
            else:
                reader=0




        # 获取内容
        text_parent = safe_get_element_by_xpath(driver, './/div[@class="art-con2"]')
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
        with open('../Policy/csv/吉林.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(pub_time)] + [str(driver.current_url)] + [str(texts)] + [str(source)]+[str(reader)])


if __name__ == '__main__':
    #initCsv()
    # getUrls()
    getHtml()
