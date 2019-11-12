import json
from multiprocessing import Pool            #进程池

import requests
from requests.exceptions import  RequestException
import re

def get_one_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}     #访问猫眼要加headers，不然不让爬
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)    #re.S表示匹配任意字符
    items = re.findall(pattern, html)
    for item in items:
        yield {                                                     #yield 被称为生成器，占用内存少，只输出迭代结果
            "rank": item[0],
            "image": item[1],
            "title": item[2],
            "actors": item[3].strip()[3:],
            "releasetime": item[4].strip()[5:],
            "score": item[5] + item[6]
        }

def write_to_file(content):
    with open("result.text", "a", encoding="utf-8") as f:
        f.write(json.dumps(content, ensure_ascii=False) + "\n")    #显示中文，而非编码
        f.close()

def main(offset):
    url = "https://maoyan.com/board/4?offset=" + str(offset)
    html = get_one_page(url)
    # print(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == "__main__":
    # for i in range(10):
    #     main(i * 10)
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])         #多进程，此处两行和上方两行效果一样，但是抓去更快，就是因为不是单进程所以抓去网页的顺序会相对错乱

# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
# response = requests.get("https://maoyan.com/board", headers = headers)
# print(response.text)