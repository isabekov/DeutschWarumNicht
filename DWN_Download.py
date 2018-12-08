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
url_top = 'https://www.dw.com/ru/учить-немецкий/deutsch-warum-nicht/s-2561'
response = urllib.request.urlopen(utf8_convert(url_top))
data = response.read()      # a `bytes` object
text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
soup = BeautifulSoup(text, 'html.parser')

courses_rss = list()
for tag in soup.find_all('div', {"class": "linkList intern"}):
    print('Tag:', tag.a['href'])
    print(tag.h2.contents[0].strip().split('|')[0])
    courses_rss.append((tag.a['href'], tag.h2.contents[0].strip().split('|')[0]))

url = courses_rss[0][0]
#print(urllib.__dict__)
response = urllib.request.urlopen(url)
data = response.read()      # a `bytes` object
text = data.decode('utf-8') # a `str`; this step can't be used if data is binary

#print(text)
doc = xmltodict.parse(text)

print(doc['rss']['channel']['item'][0]['enclosure']['@url'])
print(doc['rss']['channel']['item'][0]['title'])

#if not os.path.exists(dir_parent):
#    os.makedirs(dir_parent)
    
buch = url = courses_rss[0][1]
#if not os.path.exists(os.path.join(dir_parent, buch)):
#    os.makedirs(os.path.join(dir_parent, buch))

lektion = doc['rss']['channel']['item'][0]['title']
if not os.path.exists(os.path.join(dir_parent, buch, lektion)):
    os.makedirs(os.path.join(dir_parent, buch, lektion))

url_mp3 = doc['rss']['channel']['item'][0]['enclosure']['@url']
file_name = os.path.basename(url_mp3)
print('File: ', file_name, '\n')
urllib.request.urlretrieve(url_mp3, os.path.join(dir_parent, buch, lektion, file_name))

items = doc['rss']['channel']['item']
for item in items:
    print(item['guid']['#text'])

# Sample Lektion
url = items[0]['guid']['#text']
url_spl = urllib.parse.urlsplit(url)
url_spllist = list(url_spl)
print('URL original:')
print(url_spllist, '\n')

print('URL quoted (solution to UTF-8):')
url_spllist[2] = urllib.parse.quote(url_spllist[2])
print(url_spllist, '\n')

print('URL quoted:')
url_quo = urllib.parse.urlunsplit(url_spllist)
print(url_quo, '\n')

response = urllib.request.urlopen(url_quo)
data = response.read()      # a `bytes` object
text = data.decode('utf-8') # a `str`; this step can't be used if data is binary

soup = BeautifulSoup(text, 'html.parser')
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
