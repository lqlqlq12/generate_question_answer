import csv
import re
import time
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException

driver = webdriver.Edge()


def safe_click(driver, xpath, tick=3):
    i = 0
    while True:
        try:
            i += 1
            time.sleep(1)
            button = driver.find_element_by_xpath(xpath)
            button.click()
            break
        except StaleElementReferenceException:
            if (i > tick):
                break
            continue


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
        except StaleElementReferenceException:
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
    url_array = ['http://rst.fujian.gov.cn/']

    driver.get(url_array[0])
    # 输入框
    input = safe_get_element_by_id(driver, "selecttags")
    input.send_keys("大学生就业")

    # 搜索按钮
    button = safe_get_elements(driver, './/button')[1]
    button.click()
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])

    # 最大化，才可以看见高级搜索按钮
    driver.maximize_window()
    # 高级搜索按钮
    button2 = safe_get_elements(driver, './/a[contains(text(),"高级搜索")]')[2]
    button2.click()

    # 关键字输入框
    input2 = safe_get_element_by_xpath(driver, './/input[@id="gjssAllKey"]')
    input2.send_keys("大学生，就业")

    # 搜索按钮
    button3 = safe_get_element_by_xpath(driver, './/input[@value="搜索"]')
    button3.click()

    # 政务公开按钮
    button4 = safe_get_element_by_xpath(driver, './/ul[@id="sourceTypeTpl"]/li[5]/a')
    time.sleep(5)
    button4.click()
    print(button4.text)

    href_arrays = set()
    limit = 600

    while True:
        href_elements = safe_get_elements(driver, './/li/h2/a')
        for ele in href_elements:
            href_arrays.add(ele.get_attribute('href'))

        if len(href_arrays) > limit:
            break

        time.sleep(3)
        safe_click(driver, './/a[@class="layui-laypage-next"]')

        print(len(href_arrays))

    print(len(href_arrays))
    with open('../Policy/txt/FujianPolicy.txt', 'w') as f:
        for ele in href_arrays:
            f.write(str(ele) + '\n')


# 初始化csv
def initCsv():
    with open('../Policy/csv/福建.csv', 'a', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["时间", "网站", "内容", "来源", "浏览量"])


def getHtml():
    with open('../Policy/txt/FujianPolicy.txt', 'r') as f:
        hrefs = [line.strip() for line in f]

    for url in hrefs:
        driver.get(url)
        # div=safe_get_elements(driver,'.//div[@class="xl_tit2_l"]/span')
        # time=div[1]
        # print(time.text)
        # readers=div[2]
        # print(readers.text)

        # 获取时间
        time_element = safe_get_element_by_xpath(driver, "//*[contains(text(), '发布时间')]")
        if not time_element:
            time = ""
        else:
            time = time_element.text
            match1 = re.search(r'\d{4}-\d{2}-\d{2}', time)
            if match1:
                time = match1.group()

        print(time)

        # 获取浏览量
        readers_element = safe_get_element_by_xpath(driver, "//*[contains(text(), '浏览量')]")
        if not readers_element:
            readers=0
        else:
            readers = readers_element.text
            match2 = re.search(r'\d', readers)
            if match2:
                readers = match2.group()

        # 获取内容
        source = driver.page_source
        match3 = re.search(r'<!--正文-->([\s\S]*?)<!--正文end-->', source)
        if match3:
            content = match3.group(1)
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text()
            print(text)
        else:
            text = ""
        text = re.sub('([^\u4e00-\u9fa5\u0030-\u0039])', '.', text)

        if "大学生" not in text and "毕业生" not in text and "高校" not in text:
            continue
        # texts=safe_get_elements(driver,'.//span//text[@class="barrier-free-text"]')
        # text_element=safe_get_element_by_xpath(driver,'.//span[@barrier-free-leaf-idx="68"]')
        # texts=text_element.find_elements_by_xpath('.//br')
        # text=""
        # for item in texts:
        #     text+=str(item.text)
        # print(text)
        with open('../Policy/csv/福建.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([str(time)] + [str(driver.current_url)] + [str(text)] + ["福建省人力资源和社会保障厅"] + [str(readers)])


if __name__ == '__main__':
    initCsv()
    # getUrls()
    getHtml()
