import requests
import re
import json
from multiprocessing import Pool

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def parseOneHTML(html):
    pat = re.compile(r'<dd>.*?board-index.*?>(\d+)</i>.*?name.*?<a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>', re.S)
    items = re.findall(pat, html)
    print(items)
    for item in items:
        yield {
            "board" : item[0],
            "name" : item[1],
            "actor" : item[2].strip()[3:],
            "releasetime" : item[3].strip()[5:],
            "socre" : item[4] + item[5]
        }

def writeToFile(content):
    with open("movie.txt", "a", encoding="utf-8") as file:
        file.write(json.dumps(content, ensure_ascii=False) + '\n')

def main(offset):
    url = "http://maoyan.com/board/4?offset=" + str(offset)
    html = getHTMLText(url)
    #print(html)
    if html != "":
        for item in parseOneHTML(html):
            print(item)
            writeToFile(item)

if __name__ == '__main__':
    #for i in range(10):
    #    main(i * 10)

    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])