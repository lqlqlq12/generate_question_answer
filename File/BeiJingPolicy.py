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
    # 政策文件
    url = 'http://rsj.beijing.gov.cn/so/s?tab=zcwj&siteCode=1100000062&qt=%E5%A4%A7%E5%AD%A6%E7%94%9F%20AND%20%E5%B0%B1%E4%B8%9A&sitePath=true'
    driver.get(url)

    href_arrays = set()
    limit = 12000

    print('文件')
    while True:
        href_elements = safe_get_elements(driver, './/div[@class="title"]/a')
        for ele in href_elements:
            print(ele.get_attribute('href'))
            href_arrays.add(ele.get_attribute('href'))

        if len(href_arrays) > limit:
            break

        print(len(href_arrays))

        time.sleep(3)
        has_next = safe_click(driver, './/a[@class="next"]')
        if has_next:
            continue
        else:
            break

    # 政民互动
    print('政民')
    url = 'http://rsj.beijing.gov.cn/so/s?tab=zmhd&siteCode=1100000062&qt=%E5%A4%A7%E5%AD%A6%E7%94%9F%20AND%20%E5%B0%B1%E4%B8%9A&sitePath=true'
    driver.get(url)
    while True:
        href_elements = safe_get_elements(driver, './/div[@class="title"]/a')
        for ele in href_elements:
            print(ele.get_attribute('href'))
            href_arrays.add(ele.get_attribute('href'))

        if len(href_arrays) > limit:
            break

        print(len(href_arrays))

        time.sleep(3)
        has_next = safe_click(driver, './/a[@class="next"]')
        if has_next:
            continue
        else:
            break

    # 便民服务
    print('便民')
    url = 'http://rsj.beijing.gov.cn/so/s?tab=bmfw&siteCode=1100000062&qt=%E5%A4%A7%E5%AD%A6%E7%94%9F%20AND%20%E5%B0%B1%E4%B8%9A&sitePath=true'
    driver.get(url)
    while True:
        href_elements = safe_get_elements(driver, './/div[@class="title"]')
        for ele in href_elements:
            type = ""
            try:
                type = ele.find_element_by_tag_name('span').text
            except Exception:
                continue
            print(type)
            if type != '常见问题':
                continue

            element = ele.find_element_by_tag_name('a')
            print(element.get_attribute('href'))
            href_arrays.add(element.get_attribute('href'))

        if len(href_arrays) > limit:
            break

        print(len(href_arrays))

        time.sleep(3)
        has_next = safe_click(driver, './/a[@class="next"]')
        if has_next:
            continue
        else:
            break

    # 新闻速览
    url = "http://rsj.beijing.gov.cn/so/s?tab=xwsl&siteCode=1100000062&qt=%E5%A4%A7%E5%AD%A6%E7%94%9F%20AND%20%E5%B0%B1%E4%B8%9A&sitePath=true"
    driver.get(url)
    while True:
        href_elements = safe_get_elements(driver, './/div[@class="title"]/a')
        for ele in href_elements:
            print(ele.get_attribute('href'))
            href_arrays.add(ele.get_attribute('href'))

        if len(href_arrays) > limit:
            break

        print(len(href_arrays))

        time.sleep(3)
        has_next = safe_click(driver, './/a[@class="next"]')
        if has_next:
            continue
        else:
            break

    with open('../Policy/txt/BeiJingPolicy.txt', 'w') as f:
        for ele in href_arrays:
            f.write(str(ele) + '\n')


# 初始化csv
def initCsv():
    with open('../Policy/csv/北京.csv', 'a', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["时间", "网站", "内容", "来源"])


def getHtml():
    with open('../Policy/txt/BeiJingPolicy.txt', 'r') as f:
        hrefs = [line.strip() for line in f]

    for url in hrefs:
        try:
            driver.get(url)
        except Exception:
            continue
        if "404" in driver.title:
            print(404)
            continue
        # 获取时间
        time_element = safe_get_element_by_xpath(driver, "//*[contains(text(), '日期')]")
        if time_element:
            match=re.search(r'\d{4}-\d{2}-\d{2}',str(time_element.text))
            if match:
                print('ok')
            if not match:
                time_element=safe_get_element_by_xpath(driver, './/ol[@class="doc-info"]/li[3]/span')
        if not time_element:
            pub_time = ""
        else:
            pub_time = time_element.text
            match1 = re.search(r'\d{4}-\d{2}-\d{2}', pub_time)
            if match1:
                pub_time=match1.group()
        if pub_time=="":
            ele=safe_get_element_by_xpath(driver,'.//div[@class="info"]/span')
            if ele:
                match2=re.search(r'\d{4}-\d{2}-\d{2}', str(ele.text))
                if match2:
                    pub_time=match2.group()
        if pub_time=="":
            ele=safe_get_element_by_xpath(driver,'.//div[@class="xqrqly"]/span')
            if ele:
                match3=re.search(r'\d{4}-\d{2}-\d{2}',str(ele.text))
                if match3:
                    pub_time=match3.group()
        if pub_time=="":
            time_element = safe_get_element_by_xpath(driver, "//*[contains(text(), '时间')]")
            if time_element:
                match = re.search(r'\d{4}-\d{2}-\d{2}', str(time_element.text))
                if match:
                    pub_time=match.group()

        print(pub_time)

        # 获取来源
        source_element = safe_get_element_by_xpath(driver, "//*[contains(text(), '来源')]")
        if not source_element:
            source = "北京市人力资源和社会保障局"
        else:
            source = source_element.text
            try:
                source = str(source).split('来源')[1].strip()
            except Exception:
                source=""

        print(source)

        # 获取内容
        text_parent = safe_get_element_by_id(driver, "mainTextZoom")
        if not text_parent:
            texts = ""
        else:
            texts_element = text_parent.find_elements_by_xpath('.//*')
            texts = ""
            for item in texts_element:
                texts += str(item.text)
        if texts=="":
            text_parent = safe_get_element_by_xpath(driver, './/div[@class="view TRS_UEDITOR trs_paper_default trs_word"]')
            if not text_parent:
                texts = ""
            else:
                texts_element = text_parent.find_elements_by_xpath('.//*')
                texts = ""
                for item in texts_element:
                    texts += str(item.text)
        if texts=="":
            text_parent = safe_get_element_by_xpath(driver,'.//div[@class="view TRS_UEDITOR trs_paper_default trs_external trs_key4format"]')
            if not text_parent:
                texts = ""
            else:
                texts_element = text_parent.find_elements_by_xpath('.//*')
                texts = ""
                for item in texts_element:
                    texts += str(item.text)
        if texts=="":
            text_parent = safe_get_element_by_xpath(driver,'.//div[@class="view TRS_UEDITOR trs_paper_default trs_word trs_key4format"]')
            if not text_parent:
                texts = ""
            else:
                texts_element = text_parent.find_elements_by_xpath('.//*')
                texts = ""
                for item in texts_element:
                    texts += str(item.text)
        if texts=="":
            text_parent = safe_get_element_by_xpath(driver,'.//div[@class="view TRS_UEDITOR trs_paper_default trs_external"]')
            if not text_parent:
                texts = ""
            else:
                texts_element = text_parent.find_elements_by_xpath('.//*')
                texts = ""
                for item in texts_element:
                    texts += str(item.text)
        if texts=="":
            text_parent = safe_get_element_by_xpath(driver,'.//div[@class="sino-col-xs-12 sino-col-md-12 column sino-px-4 sino-my-3 sino-text-cont"]')
            if not text_parent:
                texts = ""
            else:
                texts_element = text_parent.find_elements_by_xpath('.//*')
                texts = ""
                for item in texts_element:
                    texts += str(item.text)
        if texts=="":
            text_parent = safe_get_element_by_xpath(driver,'.//div[@class="view TRS_UEDITOR trs_paper_default trs_web"]')
            if not text_parent:
                texts = ""
            else:
                texts_element = text_parent.find_elements_by_xpath('.//*')
                texts = ""
                for item in texts_element:
                    texts += str(item.text)

        if texts=="":
            text_parents = safe_get_elements(driver,'.//div[@class="row sino-clearfix sino-my-5 sino-border sino-p-2"]')
            if not text_parents:
                texts = ""
            else:
                for parent in text_parents:
                    texts = ""
                    texts_element = parent.find_elements_by_xpath('.//*')
                    for item in texts_element:
                        texts += str(item.text)
        texts = texts.replace('\n', '.').replace('\r', '.')
        texts = texts.replace('\t', '.').replace('\r', '.')

        if "大学生" not in texts and "毕业生" not in texts and "高校" not in texts:
            continue

        print(texts)
        with open('../Policy/csv/北京.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(pub_time)] + [str(driver.current_url)] + [str(texts)] + [str(source)])
        print(driver.current_url,'write in')


if __name__ == '__main__':
    #getUrls()
    initCsv()
    getHtml()


