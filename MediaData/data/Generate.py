import csv
import pandas as pd


# 从知乎数据提取问答对
def zhihu():
    file_path = r'D:\courses\juniorsec\social_network\lab\final\code\MediaData\data\data1.xlsx'
    data = pd.read_excel(file_path)
    data = data[data['内容'].notna()]
    data = data.drop_duplicates()
    for index, row in data.iterrows():
        # print(row)
        with open(r'D:\courses\juniorsec\social_network\lab\final\code\qa.csv', 'a', encoding='utf_8_sig',
                  newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([row['问题']] + [row['内容']] + [''] + [row['时间']] + [row['网站']])


# 从BOSS直聘提取问答对
def boos():
    template = [
        '{1}专业在{0}地区有哪些工作',
        '{1}专业在{0}地区可以找到什么工作',
        '在{0}地区{1}专业的毕业生可以找到什么工作',
        '在{0}地区{1}专业的毕业生目前有哪些岗位',
        '在{0}地区{1}专业的毕业生目前有哪些招聘信息',
    ]
    file_path = r'D:\courses\juniorsec\social_network\lab\final\code\MediaData\data\boss_processed_nondupli.xlsx'
    data = pd.read_excel(file_path)
    data = data[data['context'].notna()]
    data = data.drop_duplicates()
    for index, row in data.iterrows():
        # print(row)
        region = str(row['context']).split('  ')[1].replace('·', '-')
        # print(region)
        majors = str(row['specialty']).split('/')
        for major in majors:
            # print(major)
            question = template[index % len(template)].format(region, major)
            with open(r'D:\courses\juniorsec\social_network\lab\final\code\qa.csv', 'a', encoding='utf_8_sig',
                      newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                writer.writerow([question] + [row['context']] + [''] + [row['date']] + [row['url']])


# 从牛客数据中提取问答对
def newcoder():
    template = [
        '{1}专业在{0}地区有哪些工作',
        '{1}专业在{0}地区可以找到什么工作',
        '在{0}地区{1}专业的毕业生可以找到什么工作',
        '在{0}地区{1}专业的毕业生目前有哪些岗位',
        '在{0}地区{1}专业的毕业生目前有哪些招聘信息',
    ]
    file_path = r'D:\courses\juniorsec\social_network\lab\final\code\MediaData\data\newcorder_process_nondupli.xlsx'
    data = pd.read_excel(file_path)
    data = data[data['context'].notna()]
    data = data.drop_duplicates()
    for index, row in data.iterrows():
        # print(row)
        regions = str(row['context']).split('  ')[1].split('/')
        # print(region)
        try:
            majors = str(row['specialty']).split('/')
        except Exception:
            print()
        for region in regions:
            for major in majors:
                # print(major)
                question = template[index % len(template)].format(region, major)
                with open(r'D:\courses\juniorsec\social_network\lab\final\code\qa.csv', 'a', encoding='utf_8_sig',
                          newline='') as f:
                    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([question] + [row['context']] + [''] + [row['date']] + [row['url']])

def shixiseng():
    template = [
        '{1}专业在{0}地区有哪些工作',
        '{1}专业在{0}地区可以找到什么工作',
        '在{0}地区{1}专业的毕业生可以找到什么工作',
        '在{0}地区{1}专业的毕业生目前有哪些岗位',
        '在{0}地区{1}专业的毕业生目前有哪些招聘信息',
    ]
    file_path = r'D:\courses\juniorsec\social_network\lab\final\code\MediaData\data\newcorder_process_nondupli.xlsx'
    data = pd.read_excel(file_path)
    data = data[data['context'].notna()]
    data = data.drop_duplicates()
    for index, row in data.iterrows():
        # print(row)
        regions = str(row['context']).split('  ')[1].split('/')
        # print(regions)
        majors = str(row['specialty']).split('/')
        for region in regions:
            for major in majors:
                # print(major)
                question = template[index % len(template)].format(region, major)
                with open(r'D:\courses\juniorsec\social_network\lab\final\code\qa.csv', 'a', encoding='utf_8_sig',
                          newline='') as f:
                    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([question] + [row['context']] + [''] + [row['date']] + [row['url']])


if __name__ == '__main__':
    zhihu()
    boos()
    newcoder()
    shixiseng()
