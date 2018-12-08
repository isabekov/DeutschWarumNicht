# "Deutsch - warum nicht?" course downloader
# This code downloads all MP3 and PDF files for all explanation languages
# of the course. Comment or uncomment language to download only a subset.
# A directory hiearchy is created for every book and chapter.
# Python 3 should be used.

import urllib
import xmltodict
import os
from bs4 import BeautifulSoup

def utf8_convert(url):
    url_spl = urllib.parse.urlsplit(url)
    url_spllist = list(url_spl)
    #print('URL original:')
    #print(urlspllist, '\n')

    #print('URL quoted (solution to UTF-8):')
    url_spllist[2] = urllib.parse.quote(url_spllist[2])
    #print(url_spllist, '\n')

    #print('URL quoted:')
    url_quo = urllib.parse.urlunsplit(url_spllist)
    #print(url_quo, '\n')
    return(url_quo)

def download_lektion(unterricht, path_sammlung):
    lektion = unterricht['title']
    path_name = os.path.join(path_sammlung, lektion)
    if not os.path.exists(path_name):
        os.makedirs(path_name)

    # Download MP3 file for the Lektion
    url_mp3 = unterricht['enclosure']['@url']
    file_name = os.path.basename(url_mp3)
    print('File: ', file_name, '\n')
    urllib.request.urlretrieve(url_mp3, os.path.join(path_name, file_name))

    # Lektion
    url = unterricht['guid']['#text']
    url_quo = utf8_convert(url)

    response = urllib.request.urlopen(url_quo)
    data = response.read()
    text = data.decode('utf-8')

    soup = BeautifulSoup(text, 'html.parser')
    url_spl = urllib.parse.urlsplit(url)
    url_spllist = list(url_spl)
    for tag in soup.find_all('div', {"class": "linkList download"}):
        print('Tag:', tag.a['href'])
        url_spllist[2] = tag.a['href']
        url_spllist[3] = ''
        url_spllist[4] = ''
        url_file = urllib.parse.urlunsplit(url_spllist)
        print('URL: ', url_file)
        file_name = os.path.join(path_name, os.path.basename(url_file))
        print('File: ', file_name, '\n')
        urllib.request.urlretrieve(url_file, file_name)

def download_sammlung(book, dir_parent):
    url_buch = book[0]
    buch = book[1]

    response = urllib.request.urlopen(url_buch)
    data = response.read()
    text = data.decode('utf-8')
    doc = xmltodict.parse(text)

    print("Downloading ", doc['rss']['channel']['item'][0]['enclosure']['@url'])
    print("Book: ", doc['rss']['channel']['item'][0]['title'])

    for unterricht in doc['rss']['channel']['item']:
        download_lektion(unterricht, os.path.join(dir_parent, buch))

languages = [
#             ('DWN_Deutsch',             'https://www.dw.com/de/deutsch-lernen/deutsch-warum-nicht/s-2163'),
             ('DWN_Englisch',            'https://www.dw.com/en/learn-german/deutsch-warum-nicht/s-2548'),
#             ('DWN_Franzoesisch',        'https://www.dw.com/fr/apprendre-lallemand/deutsch-warum-nicht/s-2618'),
#             ('DWN_Spanisch',            'https://www.dw.com/es/aprender-alemán/deutsch-warum-nicht/s-4642'),
#             ('DWN_Rumänisch',           'https://www.dw.com/ro/învaţă-germană/deutsch-warum-nicht/s-2703'),
#             ('DWN_Portugiesisch',       'https://www.dw.com/pt-br/aprender-alemão/deutsch-warum-nicht/s-2595'),
             ('DWN_Russisch',            'https://www.dw.com/ru/учить-немецкий/deutsch-warum-nicht/s-2561'),
#             ('DWN_Ukrainisch',          'https://www.dw.com/uk/вивчати-німецьку/deutsch-warum-nicht/s-9958'),
#             ('DWN_Polnisch',            'https://www.dw.com/pl/nauka-niemieckiego/deutsch-warum-nicht/s-2740'),
#             ('DWN_Serbisch',            'https://www.dw.com/sr/učite-nemački/deutsch-warum-nicht/s-3787'),
#             ('DWN_Bosnisch',            'https://www.dw.com/bs/učite-njemački/deutsch-warum-nicht/s-2640'),
#             ('DWN_Kroatisch',           'https://www.dw.com/hr/učenje-njemačkog/deutsch-warum-nicht/s-3814'),
#             ('DWN_Bulgarisch',          'https://www.dw.com/bg/да-учим-немски/deutsch-warum-nicht/s-2653'),
#             ('DWN_Makedonisch',         'https://www.dw.com/mk/учење-германски/deutsch-warum-nicht/s-10224'),
#             ('DWN_Griechisch',          'https://www.dw.com/el/μαθαινω-γερμανικα/deutsch-warum-nicht/s-2726'),
#             ('DWN_Albanisch',           'https://www.dw.com/sq/mësoni-gjermanisht/deutsch-warum-nicht/s-3670'),
#             ('DWN_Persisch',            'https://www.dw.com/fa-ir/آموزش-آلمانی/deutsch-warum-nicht/s-2770'),
#             ('DWN_Dari',                'https://www.dw.com/fa-af/آموزش-زبان-آلمانی/deutsch-warum-nicht/s-11360'),
#             ('DWN_Paschtu',             'https://www.dw.com/ps/د-الما-ني-ژ-بی-زده-کړه/deutsch-warum-nicht/s-10874'),
#             ('DWN_Urdu',                'https://www.dw.com/ur/جرمن-سیکھئے/deutsch-warum-nicht/s-10928'),
#             ('DWN_Hindi',               'https://www.dw.com/hi/जर्मन-सीखिये/deutsch-warum-nicht/s-11085'),
#             ('DWN_Bengali',             'https://www.dw.com/bn/জার্মান-ভাষা-শিখুন/deutsch-warum-nicht/s-11014'),
#             ('DWN_Türkisch',            'https://www.dw.com/tr/almanca-öğrenin/deutsch-warum-nicht/s-2609'),
#             ('DWN_Arabisch',            'https://www.dw.com/ar/تعلُّم-الألمانية/deutsch-warum-nicht/s-8613'),
#             ('DWN_Amharisch',           'https://www.dw.com/am/ጀርመንኛ-መማር/deutsch-warum-nicht/s-2776'),
#             ('DWN_Swahili',             'https://www.dw.com/sw/kujifunza-kijerumani/deutsch-warum-nicht/s-2683'),
#             ('DWN_Hausa',               'https://www.dw.com/ha/koyon-jamusanci/deutsch-warum-nicht/s-3845'),
#             ('DWN_Chinesisch',          'https://www.dw.com/zh/德语天地/deutsch-warum-nicht/s-2584'),
#             ('DWN_Indonesisch',         'https://www.dw.com/id/bahasa-jerman/deutsch-warum-nicht/s-2717')
]

for sprache in languages:
    # Directory to download to
    dir_parent = sprache[0]
    # Parent page with 4 courses (books)
    url_top = sprache[1]
    response = urllib.request.urlopen(utf8_convert(url_top))
    data = response.read()
    text = data.decode('utf-8')
    soup = BeautifulSoup(text, 'html.parser')
    courses_rss = list()
    for tag in soup.find_all('div', {"class": "linkList intern"}):
        print('Tag:', tag.a['href'])
        print(tag.h2.contents[0].strip().split('|')[0])
        courses_rss.append((tag.a['href'], tag.h2.contents[0].strip().split('|')[0]))

    for book in courses_rss:
        download_sammlung(book, dir_parent)
