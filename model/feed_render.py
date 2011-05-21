#!/usr/bin/env python
#coding:utf-8


from cid import CID_WORD
from collections import namedtuple
from zsite import Zsite
from operator import itemgetter


from mblog import feed_tuple_word
CID2FEEDFUNC = {
    CID_WORD: feed_tuple_word
}


CID2FEED_ENTRY = {
    CID_WORD : ""
}



def __init__cid2feed_entry():
    for k, v in CID2FEED_ENTRY.iteritems():
        CID2FEED_ENTRY[k] = namedtuple(
            'Entry%s'%k,
            " ".join(('id cid feed_id zsite zsite_id', v))
        )

__init__cid2feed_entry()



def render_feed_entry_list(entry_list):
    result = []
    zsite_dict = Zsite.mc_get_multi(set(itemgetter(3)(entry_list)))
    for id, cid, feed_id, zsite_id in entry_list:
        args = CID2FEEDFUNC[cid](id)
        if args is False:
            continue
        cls = CID2FEED_ENTRY[cid]
        result.append(cls(id, cid, feed_id, zsite_dict[zsite_id], zsite_id, *args))
    return result

if __name__ == "__main__":
    pass


