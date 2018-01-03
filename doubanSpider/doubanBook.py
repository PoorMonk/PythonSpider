import requests
import re

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getDetailInfo(html):
    pat = re.compile(r'<li.*?cover.*?href="(.*?)".*?title="(.*?)".*?more-meta.*?author">(.*?)</span>.*?year">(.*?)</span>', re.S)
    results = re.findall(pat, html)
    print(len(results))
    for result in results:
        href, title, author, year = result
        print(href, title, author.strip(), year.strip())

if __name__ == '__main__':
    url = "https://book.douban.com/"
    html = getHTMLText(url)
    if html != "":
        getDetailInfo(html)
    else:
        print("html is null!")