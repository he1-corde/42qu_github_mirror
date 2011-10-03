#coding:utf-8
import re
from xml.sax.saxutils import unescape

def txttidy_feed43(txt):
    return txt.replace('<p><sub><i>-- Delivered by <a href="http://feed43.com/">Feed43</a> service</i></sub></p>', '')


#RE_42QU = re.compile(r''' style="([^\"]*)">(.*)$''')

def txttidy_42qu(txt):
    first_pos = txt.find('<div id="qu42"')
    if first_pos <= 0:
        tmp = txt.find('关于作者')
        if tmp >= 0:
            txt = txt[:tmp]
        first_pos = txt.rfind('<div style="border:1px')
        if first_pos <= 0:
            return txt
    txt = txt[:first_pos]
    return txt

def txttidy_wumii(txt):
    first_pos = txt.find('<table class="wumii-related-items"')
    if first_pos <= 0:
        tmp = txt.find('猜您也喜欢')
        if tmp >= 0:
            txt = txt[:tmp]
        first_pos = txt.rfind('<table')
        if first_pos <= 0:
            return txt
    txt = txt[:first_pos]
    return txt

def txttidy_other_relate(txt):
    pos = txt.find('>相关阅读推荐')
    if pos > 0:
        txt = txt[:pos]
        txt = txt[:txt.rfind('<h3')]
    return txt

def txttidy_bshare(txt):
    first_pos = txt.find('<p><a href="http://sharethis')
    if first_pos >= 0:
        txt = txt[:first_pos]
    return txt

def txttidy(txt):
    txt = unescape(txt).replace('&quot;', '"')
    txt = txttidy_other_relate(txt)
    txt = txttidy_feed43(txt)
    txt = txttidy_42qu(txt)
    txt = txttidy_wumii(txt)
    txt = txttidy_bshare(txt)
    return txt


if __name__ == '__main__':
    print txttidy("""栏目，每周精选国内最新的优秀初创企业和大家分享，初创企业可以通过微博：<a href="http://weibo.com/web20share">@web20share</a> 或者邮箱：watsonxu{at}web20share.com进行投递。转载请著名本站链接。</p>
<h3>相关阅读推荐</h3><ul><li><a href="http://www.web20share.com/2011/09/web20share-weekly-20110923.html" tit""")
    from glob import glob

    for f in reversed(sorted(glob('test/*.txt'))):
        with open(f) as infile:
            print txttidy(infile.read())
            raw_input(f)
