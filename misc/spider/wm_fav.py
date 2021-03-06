#coding:utf-8
import _env
from os.path import abspath, join
from zkit.pprint import pformat
from zkit.spider import Rolling, Fetch, GSpider, NoCacheFetch
from zkit.bot_txt import txt_wrap_by, txt_wrap_by_all
from zkit.howlong import HowLong
from zkit.htm2txt import unescape

from wm_data import SpiderWm, wm_save, wm_fav, wm_user_id

COOKIE = """auid=tpDh6RcYTnSzopBC64smkOG0wK6N%2B4hf; __utma=264742537.1854618108.1331049812.1331889152.1331919387.4; __utmz=264742537.1331049812.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); uid=ARSq0YH%2Fiaugt%2BRnLL7t6AbWY%2FOEOjsvPGq5H4oBArFO1Lg9deFTxm6vPgpm1XmFZA%3D%3D; JSESSIONID=B0F0E2108C1BC6F915C07E0B7CBF8F25.web-15; __utmb=264742537.31.10.1331919387; __utmc=264742537"""


def wm_parser(html, url):
    user = txt_wrap_by('&u=', '&', url)
    #print user
    time = txt_wrap_by('<li id="maxActionTimeInMs"  m="', '"', html)
    if time and 'm='+time not in url and int(time) > 0:
        yield wm_parser, url[:url.rfind('=')+1]+str(time)

    user_id = wm_user_id(user)
    for i in txt_wrap_by_all(' itemid="', '<p class="operating">', html):
        if 'class="content"' in i:
            id = i[:i.find('"')]

            wm = SpiderWm.get(wmid=id)
            if wm is None:
                yield wm_txt_parser, 'http://www.wumii.com/reader/article?id=%s'%id, user_id
            else:
                wm_fav(user_id, wm.id)

def wm_txt_parser(html, url, user_id):
    id = url.rsplit('=')[-1]
    name = txt_wrap_by('target="_blank">', '</a></p>', html)
    author = txt_wrap_by('">来自：', '<', html)
    link = txt_wrap_by(
        'href="',
        '"',
        txt_wrap_by('<p class="info', '</p>', html)
    )
    like = txt_wrap_by(
        'class="num-likeIt">',
        '人喜欢</a>',
        html
    )
    txt = txt_wrap_by(
        '<div class="content">',
       ' <p class="operating">',
        html
    )

    time = txt_wrap_by('<span class="time">', '</span>', html)
    wm = wm_save(id, like, name, author, link, time, txt)
    wm_fav(user_id, wm.id)

def spider(url_list):
    fetcher = NoCacheFetch(
        0,
        {
            'Cookie': COOKIE
        }
        #'/home/zuroc/tmp',
        #tuple( { 'Cookie': i.replace('Cookie:','').strip() } for i in COOKIE),
        #1,
    )
    spider = Rolling( fetcher, url_list )

    debug = False
    debug = True

    spider_runner = GSpider(spider, workers_count=10, debug=debug)
    spider_runner.start()


url_list = [
]

with open('wm_user.txt') as wm_user:
    for pos, i in enumerate(wm_user):
        i = i.strip()
        if i:
            url_list.append((wm_parser, 'http://www.wumii.com/user/article/get?type=LIKED_ITEM&u=%s&m=9331724404885'%i) , )
        #if pos > 2:
        #    break

spider(url_list)


print "over"
