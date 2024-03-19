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
    url = 'https://search1.henan.gov.cn/jrobot/search.do?_cus_lq_field_107=&_cus_eq_field_105=&_cus_eq_field_110=&_cus_pq_content=&_cus_eq_field_118=&_cus_eq_field_119=&_cus_eq_field_108=&_cus_eq_field_111=&_cus_eq_field_113=&_cus_eq_field_112=&webid=10040&pg=12&p=1&tpl=&category=&_cus_query=&_cus_pq_content=&q=%E6%AF%95%E4%B8%9A%E7%94%9F%E5%B0%B1%E4%B8%9A&pos=title&od=0&date=&date='
    driver.get(url)

    href_arrays = set()
    limit = 12000

    while True:
        href_elements = safe_get_elements(driver, './/div[@class="jsearch-result-title"]/a')
        for ele in href_elements:
            print(ele.get_attribute('href'))
            href_arrays.add(ele.get_attribute('href'))

        if len(href_arrays) > limit:
            break

        print(len(href_arrays))
        has_next = safe_click(driver, './/div[@id="pagination"]/a[last()]')
        tile = safe_get_element_by_xpath(driver, './/span[@paged="下一页"]')
        if tile:
            break
        if has_next:
            continue
        else:
            break

    with open('../Policy/txt/HeNanPolicy.txt', 'w') as f:
        for ele in href_arrays:
            f.write(str(ele) + '\n')

    for item in href_arrays:
        try:
            driver.get(item)
        except Exception:
            continue

        # 获取内容
        text_parent = safe_get_element_by_xpath(driver, './/td[@class="context6"]')
        if not text_parent:
            texts = ""
        else:
            texts_element = text_parent.find_elements_by_xpath('.//*')
            texts = ""
            for item in texts_element:
                texts += str(item.text)
            texts = texts.replace('\n', '.').replace('\r', '.')
            texts = texts.replace('\t', '.')

        if "大学生" not in texts and "毕业生" not in texts and "高校" not in texts:
            continue
        print(texts)

        # 获取时间
        context_element = safe_get_element_by_xpath(driver, './/div[@class="context"]')
        context=""
        if not context_element:
            pub_time = ""
        else:
            context = context_element.text
            match = re.search(r'\d{4}-\d{2}-\d{2}', context)
            if match:
                pub_time = match.group()
            else:
                pub_time=""
        print(pub_time)

        # 获取来源
        if not context_element:
            source = "河南省人力资源社会保障厅"
        else:
            source=context.split('时间')[0].split('：')[1].strip()
        print(source)

        # 点击量
        if not context_element:
            readers = 0
        else:
            readers = context.split('浏览')[1].split('人')[0].strip()
        print(readers)

        with open('../Policy/csv/河南.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(pub_time)] + [str(driver.current_url)] + [str(texts)] + [str(source)]+[str(readers)])
        print('write in', driver.current_url)


    href_arrays.clear()

    url = 'https://hrss.henan.gov.cn/zcwj/'
    driver.get(url)
    safe_click(driver, './/a[@onclick="pageMethod.getNewsList(1, 10, '', 165, true)"]')
    while True:
        href_elements = safe_get_elements(driver, './/tbody[@id="newsList"]/tr//a')
        pre_len = len(href_arrays)
        for ele in href_elements:
            print(ele.get_attribute('href'))
            href_arrays.add(ele.get_attribute('href'))

        if pre_len == len(href_arrays):
            break
        if len(href_arrays) > limit:
            break
        print(len(href_arrays))
        has_next = safe_click(driver, './/li[@page-rel="nextpage"]')
        if has_next:
            continue
        else:
            break

    with open('../Policy/txt/HeNanPolicy.txt', 'a') as f:
        for ele in href_arrays:
            f.write(str(ele) + '\n')

    for href in href_arrays:
        try:
            driver.get(href)
        except Exception:
            continue

        # 获取内容
        text_parent = safe_get_element_by_xpath(driver, './/td[@valign="top"]/table/tbody/tr[2]')
        if not text_parent:
            texts = ""
        else:
            texts_element = text_parent.find_elements_by_xpath('.//*')
            texts = ""
            for item in texts_element:
                texts += str(item.text)
            texts = texts.replace('\n', '.').replace('\r', '.')
            texts = texts.replace('\t', '.')

        if "大学生" not in texts and "毕业生" not in texts and "高校" not in texts:
            continue
        print(texts)

        # 获取时间
        time_element = safe_get_element_by_xpath(driver, './/div[@class="wwxx_r"][2]')
        if not time_element:
            pub_time = ""
        else:
            try:
                pub_time = time_element.text
                match=re.search(r'\d{4}年\d{2}月\d{2}日',pub_time)
                if match:
                    date_object = datetime.strptime(match.group(), "%Y年%m月%d日")
                    pub_time = date_object.strftime("%Y-%m-%d")
            except Exception:
                pub_time=""
        print('时间',pub_time)

        # 获取来源
        source="河南省人力资源和社会保障厅"
        print(source)

        readers=0

        with open('../Policy/csv/河南.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(pub_time)] + [str(driver.current_url)] + [str(texts)] + [str(source)]+[str(readers)])
        print('write in', driver.current_url)


# 初始化csv
def initCsv():
    with open('../Policy/csv/河南.csv', 'a', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["时间", "网站", "内容", "来源", "浏览量"])


def getHtml():
    with open('../Policy/HeNanPolicy.txt', 'r') as f:
        hrefs = [line.strip() for line in f]

    for url in hrefs:
        try:
            driver.get(url)
        except:
            continue
        # 获取内容
        text_parent = safe_get_element_by_xpath(driver, './/div[@id="Zoom"]')
        if not text_parent:
            texts = ""
        else:
            texts_element = text_parent.find_elements_by_xpath('.//*')
            texts = ""
            for item in texts_element:
                texts += str(item.text)
            texts = texts.replace('\n', ' ').replace('\r', ' ')
            texts = texts.replace('\t', ' ').replace('\r', ' ')

        if "大学生" not in texts and "毕业生" not in texts and "高校" not in texts:
            continue
        print(texts)

        # 获取时间
        time_element = safe_get_element_by_xpath(driver, './/div[@class="explain"]/span[1]')
        if not time_element:
            pub_time = ""
        else:
            pub_time = time_element.text
            match = re.search(r'\d{4}-\d{2}-\d{2}', pub_time)
            if match:
                pub_time = match.group()
        print(pub_time)

        # 获取来源
        source_element = safe_get_element_by_xpath(driver, './/div[@class="explain"]/span[2]')
        if not source_element:
            source = "河南省人力资源社会保障厅"
        else:
            source = source_element.text
            source = str(source).split('：')[1].strip()
        print(source)

        # 点击量
        readers_element = safe_get_element_by_xpath(driver, './/div[@id="artcount"')
        if not readers_element:
            readers = 0
        else:
            readers = readers_element.text
        print(readers)

        with open('../Policy/HeNanPolicy.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(pub_time)] + [str(driver.current_url)] + [str(texts)] + [str(source)])
        print('write in', driver.current_url)


if __name__ == '__main__':
    initCsv()
    getUrls()
    # getHtml()
