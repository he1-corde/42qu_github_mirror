#coding:utf-8
import _env
from config import ZDATA_PATH
from ptag import PTAG
from mmseg import seg_txt
from collections import defaultdict
from zkit import tofromfile
from math import log
from zkit.pprint import pprint
from os.path import basename, join, exists

CACHE_PATH = "/mnt/zdata/train/tag"

def train(filename, parser):
    fname = basename(filename)
    cache_path = join(CACHE_PATH,fname)
    if exists(cache_path):
        return 

    word2tag_count = {}
    for tag_id_list, txt in parser(filename):
        if not txt.strip():
            continue

        tag_id_set = set(tag_id_list)
        if not tag_id_set:
            continue

        for tid in tuple(tag_id_set):
            tag_id_set.update(PTAG.get(tid,()))

        word2count = defaultdict(int)
        word_list = list(seg_txt(str(txt)))
        for i in word_list:
            word2count[i] += 1

        for k, v in word2count.iteritems():
           if k not in word2tag_count:
               word2tag_count[k] = {}
           t = word2tag_count[k]
           for id in tag_id_set:
               if id not in t:
                   t[id] = 0
               t[id] += (1+log(float(v)))

    tofromfile.tofile(cache_path, word2tag_count)

#    path = join(ZDATA_PATH_TRAIN_IDF, filename)
#
#    tofile = "%s.idf"%path
#    if exists(tofile):
#        #cmd = 'scp %s work@stdyun.com:%s'%(tofile, tofile)
#        #print cmd
#        #r = envoy.run(cmd)
#        #print r.std_out
#        return
#
#    if not exists(path):
#        return
#
#    df = Df()
#    count = 0
#    with open(path) as f:
#        for txt in parser(f):
#            df.append(txt)
#            if count%1000 == 1:
#                print filename, count
#            count += 1
#
#    df.tofile(tofile)