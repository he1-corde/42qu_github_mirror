#coding:utf-8
import _env
from zkit.pprint import pprint
from json import loads
#{
#  u'board_id': 5,
#  u'comment_count': 0,
#  u'created_at': 1330917902,
#  u'file': {
#  u'bucket': u'hbimg',
#             u'farm': u'farm1',
#             u'frames': 28,
#             u'height': 263,
#             u'key': u'15bb26ccf7fd31735044a92dec42a6af640389787b280-ZJ29Av',
#             u'type': u'image/gif',
#             u'width': 350
#},
#  u'file_id': 891514,
#  u'is_private': 0,
#  u'like_count': 8,
#  u'link': u'http://marbuu.com/2011/09/19/%e6%89%93%e5%bf%83%e7%9c%bc%e9%87%8c%e7%9a%84%e5%bf%ab%e4%b9%90%e5%b0%b1%e6%98%af%e8%bf%99%e6%a0%b7%e5%ad%90%e7%9a%84/',
#  u'media_type': 0,
#  u'orig_source': None,
#  u'original': 1807084,
#  u'pin_id': 1813381,
#  u'raw_text': u'打心眼里的快乐就是这样子的.',
#  u'repin_count': 18,
#  u'source': u'marbuu.com',
#  u'text_meta': None,
#  u'user_id': 1,
#  u'via': 1812030,
#  u'via_user_id': 113388
#}

with open("/mnt/zdata/data/huaban.js") as huaban:
    for line in huaban:
        for pin in loads(line)['board']['pins']:
            txt = pin['raw_text']
            like_count = pin['like_count']
            link = pin['link']
            orig_source = pin['orig_source']
            key = pin['file']['key']
            img = "http://img.hb.aicdn.com/%s"%key
            print img
