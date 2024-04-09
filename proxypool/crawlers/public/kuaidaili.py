import json

from proxypool.crawlers.base import BaseCrawler
from proxypool.schemas.proxy import Proxy
import re
from pyquery import PyQuery as pq

BASE_URL = 'https://www.kuaidaili.com/free/{type}/{page}/'
MAX_PAGE = 3


class KuaidailiCrawler(BaseCrawler):
    """
    kuaidaili crawler, https://www.kuaidaili.com/
    """
    urls = [BASE_URL.format(type=type, page=page) for type in ('intr', 'inha') for page in range(1, MAX_PAGE + 1)]

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        # doc = pq(html)
        # script_content = doc('body > script:nth-child(10)').text()
        # print(script_content)
        # 使用正则表达式提取 fpsList 数据
        match = re.search(r'fpsList = (.*?);', html, re.S)
        if match:
            fps_list_str = match.group(1)
            # 将 fpsList 字符串转换为 json 对象
            fps_list = json.loads(fps_list_str)
            for item in fps_list:
                host = item.get('ip')
                port = item.get('port')
                if host and port:
                    yield Proxy(host=host, port=port)
        else:
            print("未找到 fpsList 数据")



if __name__ == '__main__':
    crawler = KuaidailiCrawler()
    for proxy in crawler.crawl():
        print(proxy)
