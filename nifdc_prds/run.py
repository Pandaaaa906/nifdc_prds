#!/usr/local/bin/python
import re
from datetime import datetime
from math import ceil
from urllib.parse import urljoin

from loguru import logger
from requests_html import HTMLSession

from models import NifdcPrd
from settings import WEB_USER, WEB_PASS

url_login = 'http://aoc.nifdc.org.cn/sell/loginwaiw.do?formAction=index'
urls = (
    'http://aoc.nifdc.org.cn/sell/sgoodsQuerywaiw.do?formAction=queryzc',
    'http://aoc.nifdc.org.cn/sell/sgoodsQuerywaiwTs.do?formAction=queryTs',
)

logger.add("logs/nifdc_log.log", rotation="512 MB")


def login(session, user, password):
    d = {
        'user_code': user,
        'userpwd': password,
    }
    return session.post(url_login, data=d)


def scrap_from(session, url):
    cur_page = 1
    max_page = None
    d = {
        "curPage": 2,
        "toPage": 1,
    }
    tmp = './/input[@name={!r}]/@value'
    while max_page is None or cur_page <= max_page:
        d["curPage"] = cur_page
        d["toPage"] = cur_page - 1 or cur_page + 1
        r = session.post(url, d)
        r.html.encoding = r.encoding
        rows = r.html.xpath('//table[@class="list_tab"]/tr')

        for row in rows:
            coa = row.xpath('.//td[14]/a/@href', first=True)
            d = {
                'goods_id': row.xpath(tmp.format('sgoods_id'), first=True),
                'key_id': row.xpath(tmp.format('key_id'), first=True),
                'max_purchase': row.xpath(tmp.format('zdgmshu'), first=True),
                'cat_no': row.xpath(tmp.format('sgoods_no'), first=True),
                'cn_name': row.xpath(tmp.format('sgoods_name'), first=True),
                'en_name': row.xpath(tmp.format('english_name'), first=True),
                'lot': row.xpath(tmp.format('xsBatch_no'), first=True),
                'package': row.xpath(tmp.format('standard'), first=True),
                'price': row.xpath(tmp.format('unit_price'), first=True),
                'tax': (row.xpath('.//td[10]/text()', first=True) or '').strip(),
                'usage': row.xpath(tmp.format('used'), first=True),
                'catalog': row.xpath(tmp.format('sgoods_type'), first=True),
                'storage': row.xpath(tmp.format('save_condition'), first=True),
                'coa_url': coa and urljoin(r.url, coa),
            }

            now = datetime.now()
            _ = (
                NifdcPrd.insert(**d)
                    .on_conflict(
                    conflict_target=[NifdcPrd.cat_no, NifdcPrd.lot],  # Which constraint?
                    update={**d, 'modified_at': now})
                    .execute()
            )
        # logging
        if cur_page % 50 == 0:
            logger.info(f'Scraped {cur_page} pages')
        cur_page += 1
        if max_page is not None:
            continue
        # get max page
        m = re.search(r'(?:buildPageCtrlOne001\()(\d+),(\d+),(\d+)', r.text)
        if m:
            _cur, per_page, total = m.groups()
            max_page = ceil(int(total) / int(per_page))
    logger.info(f'Url {url!r} is Done')


@logger.catch
def main():
    s = HTMLSession()
    logger.info(f'Logging in')
    login(s, WEB_USER, WEB_PASS)
    for url in urls:
        scrap_from(s, url)
    logger.info('All Done')


if __name__ == '__main__':
    NifdcPrd.create_table(safe=True)
    main()
