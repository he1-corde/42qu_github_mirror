from pyslideshare import pyslideshare
from os.path import basename

# Slideshow status : 0 if queued for conversion, 1 if converting , 2 if converted , 3 if conversion failed

def slideshare_upload(api_key, secret_key, username, password, filename, title=None):
    if title is None:
        title = basename(filename).rsplit('.', 1)[0]

    obj = pyslideshare.pyslideshare(
        {
            'api_key':api_key,
            'secret_key':secret_key
        },
        verbose=False
    )
    json = obj.upload_slideshow(username=username, password=password, slideshow_title=title, slideshow_srcfile=filename)
    slideshow_id = json.SlideShowUploaded.SlideShowID

    return slideshow_id

def slideshare_url(api_key, secret_key, id):
    obj = pyslideshare.pyslideshare(
        {
            'api_key':api_key,
            'secret_key':secret_key
        },
        verbose=False
    )
    json = obj.get_slideshow(slideshow_id=id)
    return state, json


if __name__ == '__main__':
    api_key     = 'WcxW55e6'
    secret_key  = 'L7bFrKKX'
    username    = 'zuroc'
    password    = '198662'
    id = slideshare_upload(api_key, secret_key, username, password, 'test.ppt')
    print slideshare_url(api_key, secret_key, id)
    print slideshare_url(api_key, secret_key, 10442155)