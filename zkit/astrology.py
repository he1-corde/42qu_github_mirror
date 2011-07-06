# -*- coding: utf-8 -*-
ASTROLOGY = ('', '水瓶', '双鱼', '白羊', '金牛', '双子', '巨蟹', '狮子', '处女', '天秤', '天蝎', '射手', '魔羯')

def astrology(date):
    date = date%10000
    date_mon = date//100
    date_day = date%100

    if not (date_day and date_mon):
        return 0

    if 120 < date < 219:
        return 1
    elif date < 320:
        return 2
    elif date < 420:
        return 3
    elif date < 521:
        return 4
    elif date < 621:
        return 5
    elif date < 722:
        return 6
    elif date < 823:
        return 7
    elif date < 923:
        return 8
    elif date < 1023:
        return 9
    elif date < 1122:
        return 10
    elif date < 1221:
        return 11

    return 12

if __name__ == '__main__':
    print ASTROLOGY[get_astrology(19900929)]



