from json import JSONDecodeError
import requests
import re
from bs4 import BeautifulSoup
#import urllib
from urllib.parse import urlencode
import json
import os
from hashlib import md5
from multiprocessing import Pool

from requests import RequestException

#获取索引页面（搜索关键词的页面）
def get_page_index(offset, keyword):
    try:
        data = {
            'offset': offset,
            'format': 'json',
            'keyword': keyword,
            'autoload': 'true',
            'count': 20,
            'cur_tab': 1
        }
        url = "https://www.toutiao.com/search_content/?" + urlencode(data)
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

#从索引页面中获取每一个单独的页面链接
def parse_page_index(html):
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                if item and 'article_url' in item.keys():
                    yield item.get('article_url')
    except JSONDecodeError:
        pass

#获取单个组图页面链接的内容
def get_page_detail(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        print("请求详情页出错", url)
        return None

#解析单个组图页面的内容获取每张图片的地址链接
def get_imgUrl(html):
    try:
        soup = BeautifulSoup(html, "lxml")
        title = soup.select("title")[0].get_text()
        print(title)
        pat = re.compile(r"content:.*&gt;\'", re.S) #查看发现图片链接都保存在content字段中
        res = re.search(pat, html)
        content = res.group()
        pat = re.compile(r"http(.*?)&quot", re.S)
        results = re.findall(pat, content)
        for result in results:
            newUrl = "http" + result
            yield newUrl
    except:
        pass

def download_image(url):
    print("正在下载", url)
    try:
        res = requests.get(url)
        if res.status_code == 200:
            save_image(res.content)
        return None
    except RequestException:
        print("请求图片失败", url)
        return None

def save_image(content):
    file_path = "{0}/{1}.{2}".format(os.getcwd(), md5(content).hexdigest(), "jpg")
    if not os.path.exists(file_path):
        with open(file_path, "wb") as f:
            f.write(content)

def main(offset):
    html = get_page_index(offset, "乌克兰姑娘")

    if html:
        for url in parse_page_index(html):
            html = get_page_detail(url)
            get_imgUrl(html)
            for url in get_imgUrl(html):
                download_image(url)
    #url = "https://www.toutiao.com/a6506654320115581448/"
    #html = get_page_detail(url)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [x * 20 for x in range(0, 20)])
    #main(0)