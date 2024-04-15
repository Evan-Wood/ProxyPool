import re
from datetime import datetime
from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
from loguru import logger

BASE_URL = 'https://ip.uqidata.com/freeip/{current_date}-{type}.html'
TYPES = ['socks5', 'socks4', 'isp', 'http', 'high', 'city', 'province','https']


class UqidataCrawler(BaseCrawler):
    """
    Uqidata crawler, https://ip.uqidata.com/free/index.html
    """

    def __init__(self):

        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.urls = [BASE_URL.format(current_date=self.current_date, type=type) for type in TYPES]
        self.ignore = True

    def encode(input_str):
        tmp = []
        for i in range(len(input_str)):
            tmp.append("ABCDEFGHIZ".find(input_str[i]))
        result = "".join(str(i) for i in tmp)
        result = int(result) >> 0x03
        return result

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        datas = str(doc('#main_container > div.inner > div > div > p:nth-child(2)'))
        ip_port_pattern = r'(\d+\.\d+\.\d+\.\d+):(\d+)'
        ip_ports = re.findall(ip_port_pattern, datas)
        for host, port in ip_ports:
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = UqidataCrawler()
    for proxy in crawler.crawl():
        print(proxy)
