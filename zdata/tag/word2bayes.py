#coding:utf-8
import _env
from config import ZDATA_PATH
from collections import defaultdict
from name2id import NAME2ID
from glob import glob
from config import REDIS_CONFIG
import redis
from zkit import tofromfile
from name_tidy import name_tidy
from yajl import dumps

REDIS_CONFIG['db']=1
redis = redis.Redis(**REDIS_CONFIG)


def merge():
    CACHE_PATH = "/home/work/wanfang/tag"
    for pos, i in enumerate(glob(CACHE_PATH+"/*")):
        for word, topic_freq in tofromfile.fromfile(i).iteritems():

            if len(word.strip()) <= 3:
                continue

            word = name_tidy(word)
            s = [word]
            for topic, freq in topic_freq.iteritems():
                topic = int(topic)
                s.append((topic, freq))

            print dumps(s)



if __name__ == "__main__":
    merge()
