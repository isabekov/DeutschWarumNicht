import urllib
import xmltodict
import pprint
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

dir_parent = 'DWN_Russisch'
# Parent page with 4 courses (books)
url_top = 'https://www.dw.com/ru/учить-немецкий/deutsch-warum-nicht/s-2561'
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
    url_buch = book[0]
    buch = book[1]

    response = urllib.request.urlopen(url_buch)
    data = response.read()
    text = data.decode('utf-8')
    doc = xmltodict.parse(text)

    print("Downloading ", doc['rss']['channel']['item'][0]['enclosure']['@url'])
    print("Book: ", doc['rss']['channel']['item'][0]['title'])

    for unterricht in doc['rss']['channel']['item']:
        lektion = unterricht['title']
        if not os.path.exists(os.path.join(dir_parent, buch, lektion)):
            os.makedirs(os.path.join(dir_parent, buch, lektion))

        # Download MP3 file for the Lektion
        url_mp3 = unterricht['enclosure']['@url']
        file_name = os.path.basename(url_mp3)
        print('File: ', file_name, '\n')
        urllib.request.urlretrieve(url_mp3, os.path.join(dir_parent, buch, lektion, file_name))

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
            file_name = os.path.join(dir_parent, buch, lektion, os.path.basename(url_file))
            print('File: ', file_name, '\n')
            urllib.request.urlretrieve(url_file, file_name)
