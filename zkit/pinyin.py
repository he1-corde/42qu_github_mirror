# libs.pinyin
# -*- coding: utf-8 -*-

PINYIN_INITIAL_CODEPOINTS = dict(
    a=[(0xb0, 0xa1), (0xb0, 0xc4)],
    b=[(0xb0, 0xc5), (0xb2, 0xc0)],
    c=[(0xb2, 0xc1), (0xb4, 0xed)],
    d=[(0xb4, 0xee), (0xb6, 0xe9)],
    e=[(0xb6, 0xea), (0xb7, 0xa1)],
    f=[(0xb7, 0xa2), (0xb8, 0xc0)],
    g=[(0xb8, 0xc1), (0xb9, 0xfd)],
    h=[(0xb9, 0xfe), (0xbb, 0xf6)],
    #i=[],
    j=[(0xbb, 0xf7), (0xbf, 0xa5)],
    k=[(0xbf, 0xa6), (0xc0, 0xab)],
    l=[(0xc0, 0xac), (0xc2, 0xe7)],
    m=[(0xc2, 0xe8), (0xc4, 0xc2)],
    n=[(0xc4, 0xc3), (0xc5, 0xb5)],
    o=[(0xc5, 0xb6), (0xc5, 0xbd)],
    p=[(0xc5, 0xbe), (0xc6, 0xd9)],
    q=[(0xc6, 0xda), (0xc8, 0xba)],
    r=[(0xc8, 0xbb), (0xc8, 0xf5)],
    s=[(0xc8, 0xf6), (0xcb, 0xf9)],
    t=[(0xcb, 0xfa), (0xcd, 0xd9)],
    #u=[],
    #v=[],
    w=[(0xcd, 0xda), (0xce, 0xf3)],
    x=[(0xce, 0xf4), (0xd1, 0xb8)],
    y=[(0xd1, 0xb9), (0xd4, 0xd0)],
    z=[(0xd4, 0xd1), (0xd7, 0xf9)],
)

def startswith_pinyin_initial(word):
    ranges = [PINYIN_INITIAL_CODEPOINTS.get(char) for char in word]
    def _(text):
        if not isinstance(text, unicode):
            text = text.decode('utf-8')

        ntext = len(text)
        nword = len(word)
        if nword > ntext:
            return False

        for i in xrange(len(word)):
            unicodepoint = text[i]
            if not ranges[i]: # hasn't pinyin starts with i, u, v
                return False

            start_cp, end_cp = ranges[i]
            gbk_cp = unicodepoint.encode('gbk', 'ignore')
            if len(gbk_cp) < 2:
                return False

            high_cp, low_cp = ord(gbk_cp[0]), ord(gbk_cp[1])
            if high_cp < start_cp[0] or high_cp > end_cp[0]:
                # not in zone bytes range
                return False
            if high_cp == start_cp[0] and low_cp < start_cp[1]:
                # not in start zone byte' bit range
                return False
            if high_cp == end_cp[0] and low_cp > end_cp[1]:
                # not in end zone's bit range
                return False

        return True
    return _


#####
# 以 gbk 的区码作为 key，value 为该区中的所有读音的 list，顺序与位码相同。
#
PINYIN = {
    0xb0: ['a']*(0xa2-0xa0) + ['ai']*(0xaf-0xa2) + ['an']*(0xb8-0xaf) + \
        ['ang']*(0xbb-0xb8) + ['ao']*(0xc4-0xbb) + ['ba']*(0xd6-0xc4) + \
        ['bai']*(0xdd-0xd6) + ['ban']*(0xed-0xdd) + ['bang']*(0xf9-0xed) + \
        ['bao']*(0xfe-0xf9),

    0xb1: ['bao']*(0xac-0xa0) + ['bei']*(0xbb-0xac) + ['ben']*(0xbf-0xbb) + \
        ['beng']*(0xc5-0xbf) + ['bi']*(0xdd-0xc5) + ['bian']*(0xe9-0xdd) + \
        ['biao']*(0xed-0xe9) + ['bie']*(0xf1-0xed) + ['bin']*(0xf8-0xf1) + \
        ['bing']*(0xfe-0xf8),

    0xb2: ['bing']*(0xa2-0xa0) + ['bo']*(0xb5-0xa2) + ['bu']*(0xc0-0xb5) + \
        ['ca']*(0xc1-0xc0) + ['cai']*(0xcc-0xc1) + ['can']*(0xd3-0xcc) + \
        ['cang']*(0xd8-0xd3) + ['cao']*(0xdd-0xd8) + ['ce']*(0xe2-0xdd) + \
        ['ceng']*(0xe4-0xe2) + ['cha']*(0xef-0xe4) + ['chai']*(0xf2-0xef) + \
        ['chan']*(0xfc-0xf2) + ['chang']*(0xfe-0xfc),

    0xb3: ['chang']*(0xab-0xa0) + ['chao']*(0xb4-0xab) + ['che']*(0xba-0xb4) +\
        ['chen']*(0xc4-0xba) + ['cheng']*(0xd3-0xc4) + ['chi']*(0xe3-0xd3) + \
        ['chong']*(0xe8-0xe3) + ['chou']*(0xf4-0xe8) + ['chu']*(0xfe-0xf4),

    0xb4: ['chu']*(0xa6-0xa0) + ['chuai']*(0xa7-0xa6) + ['chuan']*(0xae-0xa7)+\
        ['chuang']*(0xb4-0xae) + ['chui']*(0xb9-0xb4) + ['chun']*(0xc0-0xb9) +\
        ['chuo']*(0xc2-0xc0) + ['ci']*(0xce-0xc2) + ['cong']*(0xd4-0xce) + \
        ['cou']*(0xd5-0xd4) + ['cu']*(0xd9-0xd5) + ['cuan']*(0xdc-0xd9) + \
        ['cui']*(0xe4-0xdc) + ['cun']*(0xe7-0xe4) + ['cuo']*(0xed-0xe7) + \
        ['da']*(0xf3-0xed) + ['dai']*(0xfe-0xf3),

    0xb5: ['dai']*(0xa1-0xa0) + ['dan']*(0xb0-0xa1) + ['dang']*(0xb5-0xb0) + \
        ['dao']*(0xc1-0xb5) + ['de']*(0xc4-0xc1) + ['deng']*(0xcb-0xc4) + \
        ['di']*(0xde-0xcb) + ['dian']*(0xee-0xde) + ['diao']*(0xf7-0xee) + \
        ['die']*(0xfe-0xf7),

    0xb6: ['ding']*(0xa9-0xa0) + ['diu']*(0xaa-0xa9) + ['dong']*(0xb4-0xaa) + \
        ['dou']*(0xbc-0xb4) + ['du']*(0xca-0xbc) + ['duan']*(0xd0-0xca) + \
        ['dui']*(0xd4-0xd0) + ['dun']*(0xdd-0xd4) + ['duo']*(0xe9-0xdd) + \
        ['e']*(0xf6-0xe9) + ['en']*(0xf7-0xf6) + ['er']*(0xfe-0xf7),

    0xb7: ['er']*(0xa1-0xa0) + ['fa']*(0xa9-0xa1) + ['fan']*(0xba-0xa9) + \
        ['fang']*(0xc5-0xba) + ['fei']*(0xd1-0xc5) + ['fen']*(0xe0-0xd1) + \
        ['feng']*(0xef-0xe0) + ['fo']*(0xf0-0xef) + ['fou']*(0xf1-0xf0) + \
        ['fu']*(0xfe-0xf1),

    0xb8: ['fu']*(0xc0-0xa0) + ['ga']*(0xc2-0xc0) + ['gai']*(0xc8-0xc2) + \
        ['gan']*(0xd3-0xc8) + ['gang']*(0xdc-0xd3) + ['gao']*(0xe6-0xdc) + \
        ['ge']*(0xf7-0xe6) + ['gei']*(0xf8-0xf7) + ['gen']*(0xfa-0xf8) + \
        ['geng']*(0xfe-0xfa),

    0xb9: ['geng']*(0xa3-0xa0) + ['gong']*(0xb2-0xa3) + ['gou']*(0xbb-0xb2) + \
        ['gu']*(0xcd-0xbb) + ['gua']*(0xd3-0xcd) + ['guai']*(0xd6-0xd3) + \
        ['guan']*(0xe1-0xd6) + ['guang']*(0xe4-0xe1) + ['gui']*(0xf4-0xe4) + \
        ['gun']*(0xf7-0xf4) + ['guo']*(0xfd-0xf7) + ['ha']*(0xfe-0xfd),

    0xba: ['hai']*(0xa7-0xa0) + ['han']*(0xba-0xa7) + ['hang']*(0xbd-0xba) + \
        ['hao']*(0xc6-0xbd) + ['he']*(0xd8-0xc6) + ['hei']*(0xda-0xd8) + \
        ['hen']*(0xde-0xda) + ['heng']*(0xe3-0xde) + ['hong']*(0xec-0xe3) + \
        ['hou']*(0xf3-0xec) + ['hu']*(0xfe-0xf3),

    0xbb: ['hu']*(0xa7-0xa0) + ['hua']*(0xb0-0xa7) + ['huai']*(0xb5-0xb0) + \
        ['huan']*(0xc3-0xb5) + ['huang']*(0xd1-0xc3) + ['hui']*(0xe6-0xd1) + \
        ['hun']*(0xec-0xe6) + ['huo']*(0xf6-0xec) + ['ji']*(0xfe-0xf6),

    0xbc: ['ji']*(0xcd-0xa0) + ['jia']*(0xde-0xcd) + ['jian']*(0xfe-0xde),

    0xbd: ['jian']*(0xa8-0xa0) + ['jiang']*(0xb5-0xa8) + ['jiao']*(0xd1-0xb5)+\
        ['jie']*(0xec-0xd1) + ['jin']*(0xfe-0xec),

    0xbe: ['jin']*(0xa2-0xa0) + ['jing']*(0xbb-0xa2) + ['jiong']*(0xbd-0xbb) +\
        ['jiu']*(0xce-0xbd) + ['ju']*(0xe7-0xce) + ['juan']*(0xee-0xe7) + \
        ['jue']*(0xf8-0xee) + ['jun']*(0xfe-0xf8),

    0xbf: ['jun']*(0xa5-0xa0) + ['ka']*(0xa9-0xa5) + ['kai']*(0xae-0xa9) + \
        ['kan']*(0xb4-0xae) + ['kang']*(0xbb-0xb4) + ['kao']*(0xbf-0xbb) + \
        ['ke']*(0xce-0xbf) + ['ken']*(0xd2-0xce) + ['keng']*(0xd4-0xd2) + \
        ['kong']*(0xd8-0xd4) + ['kou']*(0xdc-0xd8) + ['ku']*(0xe3-0xdc) + \
        ['kua']*(0xe8-0xe3) + ['kuai']*(0xec-0xe8) + ['kuan']*(0xee-0xec) + \
        ['kuang']*(0xf6-0xee) + ['kui']*(0xfe-0xf6),

    0xc0: ['kui']*(0xa3-0xa0) + ['kun']*(0xa7-0xa3) + ['kuo']*(0xab-0xa7) + \
        ['la']*(0xb2-0xab) + ['lai']*(0xb5-0xb2) + ['lan']*(0xc4-0xb5) + \
        ['lang']*(0xcb-0xc4) + ['lao']*(0xd4-0xcb) + ['le']*(0xd6-0xd4) + \
        ['lei']*(0xe1-0xd6) + ['leng']*(0xe4-0xe1) + ['li']*(0xfe-0xe4),

    0xc1: ['li']*(0xa8-0xa0) + ['lia']*(0xa9-0xa8) + ['lian']*(0xb7-0xa9) + \
        ['liang']*(0xc2-0xb7) + ['liao']*(0xcf-0xc2) + ['lie']*(0xd4-0xcf) + \
        ['lin']*(0xe0-0xd4) + ['ling']*(0xee-0xe0) + ['liu']*(0xf9-0xee) + \
        ['long']*(0xfe-0xf9),

    0xc2: ['long']*(0xa4-0xa0) + ['lou']*(0xaa-0xa4) + ['lu']*(0xbe-0xaa) + \
        ['lv']*(0xcc-0xbe) + ['luan']*(0xd2-0xcc) + ['lue']*(0xd4-0xd2) + \
        ['lun']*(0xdb-0xd4) + ['luo']*(0xe7-0xdb) + ['ma']*(0xf0-0xe7) + \
        ['mai']*(0xf6-0xf0) + ['man']*(0xfe-0xf6),

    0xc3: ['man']*(0xa1-0xa0) + ['mang']*(0xa7-0xa1) + ['mao']*(0xb3-0xa7) + \
        ['me']*(0xb4-0xb3) + ['mei']*(0xc4-0xb4) + ['men']*(0xc7-0xc4) + \
        ['meng']*(0xcf-0xc7) + ['mi']*(0xdd-0xcf) + ['mian']*(0xe6-0xdd) + \
        ['miao']*(0xee-0xe6) + ['mie']*(0xf0-0xee) + ['min']*(0xf6-0xf0) + \
        ['ming']*(0xfc-0xf6) + ['miu']*(0xfd-0xfc) + ['mo']*(0xfe-0xfd),

    0xc4: ['mo']*(0xb0-0xa0) + ['mou']*(0xb3-0xb0) + ['mu']*(0xc2-0xb3) + \
        ['na']*(0xc9-0xc2) + ['nai']*(0xce-0xc9) + ['nan']*(0xd1-0xce) + \
        ['nang']*(0xd2-0xd1) + ['nao']*(0xd7-0xd2) + ['ne']*(0xd8-0xd7) + \
        ['nei']*(0xda-0xd8) + ['nen']*(0xdb-0xda) + ['neng']*(0xdc-0xdb) + \
        ['ni']*(0xe7-0xdc) + ['nian']*(0xee-0xe7) + ['niang']*(0xf0-0xee) + \
        ['niao']*(0xf2-0xf0) + ['nie']*(0xf9-0xf2) + ['nin']*(0xfa-0xf9) + \
        ['ning']*(0xfe-0xfa),

    0xc5: ['ning']*(0xa2-0xa0) + ['niu']*(0xa6-0xa2) + ['nong']*(0xaa-0xa6) + \
        ['nu']*(0xad-0xaa) + ['nv']*(0xae-0xad) + ['nuan']*(0xaf-0xae) + \
        ['nue']*(0xb1-0xaf) + ['nuo']*(0xb5-0xb1) + ['o']*(0xb6-0xb5) + \
        ['ou']*(0xbd-0xb6) + ['pa']*(0xc3-0xbd) + ['pai']*(0xc9-0xc3) + \
        ['pan']*(0xd1-0xc9) + ['pang']*(0xd6-0xd1) + ['pao']*(0xdd-0xd6) + \
        ['pei']*(0xe6-0xdd) + ['pen']*(0xe8-0xe6) + ['peng']*(0xf6-0xe8) + \
        ['pi']*(0xfe-0xf6),

    0xc6: ['pi']*(0xa9-0xa0) + ['pian']*(0xad-0xa9) + ['piao']*(0xb1-0xad) + \
        ['pie']*(0xb3-0xb1) + ['pin']*(0xb8-0xb3) + ['ping']*(0xc1-0xb8) + \
        ['po']*(0xc9-0xc1) + ['pou']*(0xca-0xc9) + ['pu']*(0xd9-0xca) + \
        ['qi']*(0xfd-0xd9) + ['qia']*(0xfe-0xfd),

    0xc7: ['qia']*(0xa2-0xa0) + ['qian']*(0xb8-0xa2) + ['qiang']*(0xc0-0xb8) +\
        ['qiao']*(0xcf-0xc0) + ['qie']*(0xd4-0xcf) + ['qin']*(0xdf-0xd4) + \
        ['qing']*(0xec-0xdf) + ['qiong']*(0xee-0xec) + ['qiu']*(0xf6-0xee) + \
        ['qu']*(0xfe-0xf6),

    0xc8: ['qu']*(0xa5-0xa0) + ['quan']*(0xb0-0xa5) + ['que']*(0xb8-0xb0) + \
        ['qun']*(0xba-0xb8) + ['ran']*(0xbe-0xba) + ['rang']*(0xc3-0xbe) + \
        ['rao']*(0xc6-0xc3) + ['re']*(0xc8-0xc6) + ['ren']*(0xd2-0xc8) + \
        ['reng']*(0xd4-0xd2) + ['ri']*(0xd5-0xd4) + ['rong']*(0xdf-0xd5) + \
        ['rou']*(0xe2-0xdf) + ['ru']*(0xec-0xe2) + ['ruan']*(0xee-0xec) + \
        ['rui']*(0xf1-0xee) + ['run']*(0xf3-0xf1) + ['ruo']*(0xf5-0xf3) + \
        ['sa']*(0xf8-0xf5) + ['sai']*(0xfc-0xf8) + ['san']*(0xfe-0xfc),

    0xc9: ['san']*(0xa2-0xa0) + ['sang']*(0xa5-0xa2) + ['sao']*(0xa9-0xa5) + \
        ['se']*(0xac-0xa9) + ['sen']*(0xae-0xac) + ['sha']*(0xb7-0xae) + \
        ['shai']*(0xb9-0xb7) + ['shan']*(0xc9-0xb9) + ['shang']*(0xd1-0xc9) + \
        ['shao']*(0xdc-0xd1) + ['she']*(0xe8-0xdc) + ['shen']*(0xf8-0xe8) + \
        ['sheng']*(0xfe-0xf8),

    0xca: ['sheng']*(0xa5-0xa0) + ['shi']*(0xd4-0xa5) + ['shou']*(0xde-0xd4) +\
        ['shu']*(0xfe-0xde),

    0xcb: ['shu']*(0xa1-0xa0) + ['shua']*(0xa3-0xa1) + ['shuai']*(0xa7-0xa3) +\
        ['shuan']*(0xa9-0xa7) + ['shuang']*(0xac-0xa9) + ['shui']*(0xb0-0xac)+\
        ['shun']*(0xb4-0xb0) + ['shuo']*(0xb8-0xb4) + ['si']*(0xc8-0xb8) + \
        ['song']*(0xd0-0xc8) + ['sou']*(0xd4-0xd0) + ['su']*(0xe0-0xd4) + \
        ['suan']*(0xe3-0xe0) + ['sui']*(0xee-0xe3) + ['sun']*(0xf1-0xee) + \
        ['suo']*(0xf9-0xf1) + ['ta']*(0xfe-0xf9),

    0xcc: ['ta']*(0xa4-0xa0) + ['tai']*(0xad-0xa4) + ['tan']*(0xbf-0xad) + \
        ['tang']*(0xcc-0xbf) + ['tao']*(0xd7-0xcc) + ['te']*(0xd8-0xd7) + \
        ['teng']*(0xdc-0xd8) + ['ti']*(0xeb-0xdc) + ['tian']*(0xf3-0xeb) + \
        ['tiao']*(0xf8-0xf3) + ['tie']*(0xfb-0xf8) + ['ting']*(0xfe-0xfb),

    0xcd: ['ting']*(0xa7-0xa0) + ['tong']*(0xb4-0xa7) + ['tou']*(0xb8-0xb4) + \
        ['tu']*(0xc4-0xb8) + ['tuan']*(0xc5-0xc4) + ['tui']*(0xcb-0xc5) + \
        ['tun']*(0xce-0xcb) + ['tuo']*(0xd9-0xce) + ['wa']*(0xe0-0xd9) + \
        ['wai']*(0xe2-0xe0) + ['wan']*(0xf3-0xe2) + ['wang']*(0xfd-0xf3) + \
        ['wei']*(0xfe-0xfd),

    0xce: ['wei']*(0xc0-0xa0) + ['wen']*(0xca-0xc0) + ['weng']*(0xcd-0xca) + \
        ['wo']*(0xd6-0xcd) + ['wu']*(0xf3-0xd6) + ['xi']*(0xfe-0xf3),

    0xcf: ['xi']*(0xb8-0xa0) + ['xia']*(0xc5-0xb8) + ['xian']*(0xdf-0xc5) + \
        ['xiang']*(0xf3-0xdf) + ['xiao']*(0xfe-0xf3),

    0xd0: ['xiao']*(0xa7-0xa0) + ['xie']*(0xbc-0xa7) + ['xin']*(0xc6-0xbc) + \
        ['xing']*(0xd5-0xc6) + ['xiong']*(0xdc-0xd5) + ['xiu']*(0xe5-0xdc) + \
        ['xu']*(0xf8-0xe5) + ['xuan']*(0xfe-0xf8),

    0xd1: ['xuan']*(0xa4-0xa0) + ['xue']*(0xaa-0xa4) + ['xun']*(0xb8-0xaa) + \
        ['ya']*(0xc8-0xb8) + ['yan']*(0xe9-0xc8) + ['yang']*(0xfa-0xe9) + \
        ['yao']*(0xfe-0xfa),

    0xd2: ['yao']*(0xab-0xa0) + ['ye']*(0xba-0xab) + ['yi']*(0xef-0xba) + \
        ['yin']*(0xfe-0xef),

    0xd3: ['yin']*(0xa1-0xa0) + ['ying']*(0xb3-0xa1) + ['yo']*(0xb4-0xb3) + \
        ['yong']*(0xc3-0xb4) + ['you']*(0xd7-0xc3) + ['yu']*(0xfe-0xd7),

    0xd4: ['yu']*(0xa6-0xa0) + ['yuan']*(0xba-0xa6) + ['yue']*(0xc4-0xba) + \
        ['yun']*(0xd0-0xc4) + ['za']*(0xd3-0xd0) + ['zai']*(0xda-0xd3) + \
        ['zan']*(0xde-0xda) + ['zang']*(0xe1-0xde) + ['zao']*(0xef-0xe1) + \
        ['ze']*(0xf3-0xef) + ['zei']*(0xf4-0xf3) + ['zen']*(0xf5-0xf4) + \
        ['zeng']*(0xf9-0xf5) + ['zha']*(0xfe-0xf9),

    0xd5: ['zha']*(0xa9-0xa0) + ['zhai']*(0xaf-0xa9) + ['zhan']*(0xc0-0xaf) + \
        ['zhang']*(0xcf-0xc0) + ['zhao']*(0xd9-0xcf) + ['zhe']*(0xe3-0xd9) + \
        ['zhen']*(0xf3-0xe3) + ['zheng']*(0xfe-0xf3),

    0xd6: ['zheng']*(0xa4-0xa0) + ['zhi']*(0xcf-0xa4) + ['zhong']*(0xda-0xcf)+\
        ['zhou']*(0xe8-0xda) + ['zhu']*(0xfe-0xe8),

    0xd7: ['zhu']*(0xa4-0xa0) + ['zhua']*(0xa6-0xa4) + ['zhuai']*(0xa7-0xa6) +\
        ['zhuan']*(0xad-0xa7) + ['zhuang']*(0xb4-0xad) + ['zhui']*(0xba-0xb4)+\
        ['zhun']*(0xbc-0xba) + ['zhuo']*(0xc7-0xbc) + ['zi']*(0xd6-0xc7) + \
        ['zong']*(0xdd-0xd6) + ['zou']*(0xe1-0xdd) + ['zu']*(0xe9-0xe1) + \
        ['zuan']*(0xeb-0xe9) + ['zui']*(0xef-0xeb) + ['zun']*(0xf1-0xef) + \
        ['zuo']*(0xf9-0xf1)
}

def pinyin_by_char(char):
    if not isinstance(char, unicode):
        char = char.decode('utf-8')

    gbk = char.encode('gbk', 'ignore')
    if len(gbk) < 2:
        return

    highcp, lowcp = ord(gbk[0]), ord(gbk[1])
    bits = PINYIN.get(highcp)
    if not bits:
        return

    return bits[lowcp-0xa0-1] # 0xa0 is nope in bits, the first element is 0xa1

def pinyin_by_str(text):
    if not isinstance(text, unicode):
        text = text.decode('utf-8')

    pinyin_list = []
    for char in text:
        pinyin = pinyin_by_char(char)
        if pinyin:
            pinyin_list.append(pinyin)
    return ''.join(pinyin_list)

if __name__ == '__main__':
    print dir(startswith_pinyin_initial('zh'))
    print startswith_pinyin_initial('zh')('张沈鹏')
    print startswith_pinyin_initial('z')('沈鹏')
    print startswith_pinyin_initial('s')('沈鹏'), '!!!!'
    print startswith_pinyin_initial('sh')('沈鹏')
    print pinyin_by_str('张沈鹏')
