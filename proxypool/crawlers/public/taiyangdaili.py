from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
from pyquery import PyQuery as pq

BaseUrl = 'http://ip.tyhttp.com/{num}'
MAX_PAGE = 3


class TaiyangdailiCrawler(BaseCrawler):
    """
    taiyangdaili crawler, http://www.taiyanghttp.com/free/
    """
    urls = [BaseUrl.format(num=i) for i in range(1, 6)]

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        trs = doc('div.list').items()
        for tr in trs:
            host = tr.find('div.td.td-4').text()
            port = tr.find('div.td.td-2').text()[0:4]
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = TaiyangdailiCrawler()
    for proxy in crawler.crawl():
        print(proxy)
