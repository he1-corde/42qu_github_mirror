#coding:utf-8


VIDEO_CID_YOUKU = 1
VIDEO_CID_TUDOU = 2
VIDEO_CID_SINA = 3
VIDEO_CID_SLIDESHARE = 4

LINK_AUTOPLAY_YOUKU = "http://static.youku.com/v/swf/qplayer.swf?VideoIDS=%s=&isShowRelatedVideo=false&showAd=0&winType=interior&isAutoPlay=true"

LINK_AUTOPLAY_TUDOU = "http://www.tudou.com/v/%s&autoPlay=true/v.swf"

LINK_AUTOPLAY_SINA = "http://p.you.video.sina.com.cn/swf/quotePlayer20110627_V4_4_41_20.swf?autoplay=1&vid=%s&uid=%s"

LINK_SLIDESHARE = "%s/swf/ssplayer2.swf?doc=%%s&rel=0"%FS_URL


_HTM_SWF = '''<embed src="%s" quality="high" class="video" allowfullscreen="true" align="middle" allowScriptAccess="sameDomain" type="application/x-shockwave-flash" wmode= "Opaque"></embed>'''

HTM_YOUKU = _HTM_SWF%"http://static.youku.com/v/swf/qplayer.swf?VideoIDS=%s=&isShowRelatedVideo=false&showAd=0&winType=interior"

HTM_AUTOPLAY_YOUKU = _HTM_SWF%LINK_AUTOPLAY_YOUKU

HTM_TUDOU = _HTM_SWF%"http://www.tudou.com/v/%s/v.swf"

HTM_AUTOPLAY_TUDOU = _HTM_SWF%LINK_AUTOPLAY_TUDOU

HTM_AUTOPLAY_SINA = _HTM_SWF%LINK_AUTOPLAY_SINA

HTM_SINA = _HTM_SWF%"http://p.you.video.sina.com.cn/swf/quotePlayer20110627_V4_4_41_20.swf?vid=%s&uid=%s&autoPlay=0"

HTM_SLIDESHARE = _HTM_SWF%LINK_SLIDESHARE



VIDEO_CID2HTM = {
    VIDEO_CID_YOUKU:HTM_YOUKU,
    VIDEO_CID_TUDOU:HTM_TUDOU,
    VIDEO_CID_SINA:HTM_SINA,
    VIDEO_CID_SLIDESHARE:HTM_SLIDESHARE,
}

VIDEO_CID2HTM_AUTOPLAY = {
    VIDEO_CID_YOUKU:HTM_AUTOPLAY_YOUKU,
    VIDEO_CID_TUDOU:HTM_AUTOPLAY_TUDOU,
    VIDEO_CID_SINA:HTM_AUTOPLAY_SINA,
    VIDEO_CID_SLIDESHARE:HTM_SLIDESHARE,
}
def video_filter(url):
    if url.startswith('http://v.youku.com/v_show/id_'):
        video = url[29:url.rfind('.')]
        video_site = VIDEO_CID_YOUKU
    elif url.startswith('http://player.youku.com/player.php/sid/'):
        video = url[39:url.find('/', 39)]
        video_site = VIDEO_CID_YOUKU
    elif url.startswith('http://www.tudou.com/programs/view/'):
        video = url[35:].rstrip('/')
        video_site = VIDEO_CID_TUDOU
    elif url.startswith('http://video.sina.com.cn/v/b/'):
        video = url[29:url.rfind('.')]
        video_site = VIDEO_CID_SINA
    elif url.startswith('http://static.slidesharecdn.com/swf/ssplayer2.swf?'):
        begin = url.find('doc=')+4
        video = url[begin:url.find('&', begin)]
        video_site = VIDEO_CID_SLIDESHARE
    else:
        video = None
        video_site = None
    return video, video_site

def video_htm_autoplay(cid, id):
    if cid == VIDEO_CID_SINA:
        return VIDEO_CID2HTM_AUTOPLAY[cid] % tuple(video_uri(id).split('-'))
    return VIDEO_CID2HTM_AUTOPLAY[cid] % video_uri(id)

def video_htm(cid, id):
    if cid == VIDEO_CID_SINA:
        return VIDEO_CID2HTM[cid] % tuple(video_uri(id).split('-'))
    return VIDEO_CID2HTM[cid] % video_uri(id)

if __name__ == "__main__":
    pass



