
import re
import jieba
import requests
from bs4 import BeautifulSoup
from collections import Counter


# def read_file(file_path):
#     with open('C:\\Users\\Lenovo\Desktop\\前端基础\\12306\\news3.txt', 'r', encoding='utf-8') as file:
#         text = file.read()
#     return text


def process_data(url):
    # 定义URL

    # 发送GET请求并获取响应
    response = requests.get(url)

    # 确定编码
    encoding = response.encoding if 'charset' in response.headers.get(
        'content-type', '').lower() else None

    # 使用BeautifulSoup解析响应文本
    soup = BeautifulSoup(response.content, 'html.parser',
                         from_encoding=encoding)

    # 查找ID为"UCAP-CONTENT"的DIV
    div = soup.find('div', {'id': 'UCAP-CONTENT'})
    # div = soup.find('div', {'class': 'view'})

    # 获取DIV中的文本内容
    content = div.text

    def remove_html_tags(content):
        pattern = re.compile(r'<[^>]+>', re.S)
        text = re.sub(pattern, '', content)
        return text

    def remove_punctuation(text):
        punctuation = r'[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：；《）《》“”()»〔〕-]+'
        text = re.sub(punctuation, '', text)
        return text

    def word_segmentation(text):
        seg_list = jieba.cut(text)
        return seg_list

    def count_word_frequency(seg_list):
        word_count = Counter(seg_list)
        return word_count

    def output_top_words(word_count, n=20):
        top_words = word_count.most_common(n)
        for word, count in top_words:
            print(f'{word}: {count}')

    # def save_word_frequency(word_count, file_path):
    #     word_list = []
    #     for word, count in word_count.items():
    #         word_dict = {'word': word, 'count': count}
    #         word_list.append(word_dict)
    #     # print('----------------------')
    #     # print(word_list)
    #     return word_list
    def save_word_frequency(word_count, file_path):
        word_list = []
        for word, count in word_count.items():
            word_dict = {'word': word, 'count': count}
            word_list.append(word_dict)
            

        # 对 word_list 按照 count 键的值进行排序
        word_list.sort(key=lambda x: x['count'], reverse=True)

        # 选择前六项作为返回结果
        top_six_words = word_list[1:21]

        return top_six_words

    # def save_word_frequency(word_count, file_path):
    #     with open(file_path, 'w', encoding='utf-8') as file:
    #         for word, count in word_count.items():
    #             file.write(f'{word},{count}\n')

    # 读取文本文件
    # text = read_file('input.txt')

    # 去除HTML标签
    text = remove_html_tags(content)

    # 去除标点符号
    text = remove_punctuation(text)

    # 分词
    seg_list = word_segmentation(text)

    # 统计词频
    word_count = count_word_frequency(seg_list)

    # 输出词频最高的20个词
    output_top_words(word_count, n=20)

    # 保存词频结果
    return save_word_frequency(word_count, 'words.txt')
    print('------------------')
    print(save_word_frequency(word_count, 'words.txt'))
