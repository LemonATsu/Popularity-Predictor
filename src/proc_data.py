 # -*- coding: utf-8 -*-
import numpy as np
import re
from bs4 import BeautifulSoup

def parse_html(text):
    text = BeautifulSoup(text, 'html.parser')

    if text.find('div', attrs={'class' : 'see-also'}):    
        text.find('div', attrs={'class' : 'see-also'}).decompose()  
    if text.find('div', attrs={'class' : 'bonus-content'}):
        text.find('div', attrs={'class' : 'bonus-content'}).decompose()
    if text.findAll('div', attrs={'class' : 'meta'}):
        [meta.decompose() for meta in text.findAll('div', attrs={'class' : 'meta'})]

    author = text.find('span', attrs={'class': 'author_name'})
    title = text.find('h1', attrs={'class': 'title'}).get_text()
    content = []
    
    ps = text.findAll('p')
    for p in ps:
        content.append(p.get_text())

    try:
        content = author.join(content)
    except :
        content = "".join(content)
        
    r = '(?::|;|=|X)(?:-)?(?:\)|\(|D|P)'
    emoticons = re.findall(r, content)
    content = re.sub(r, '', content)
    
    content = re.sub('[\W]+', ' ', content.lower()) + ' ' + ' '.join(emoticons).replace('-','')
    title = re.sub('[\W]+', ' ', title.lower()) + ' ' + ' '.join(emoticons).replace('-','')

    return title + " " + content

def parse_raw(raw_data):
    parsed = np.empty((raw_data.shape[0], 2), dtype=object)

    for r in range(raw_data.shape[0]):
        title, content = (parse_html(raw_data[r]))
        parsed[r, 0] = title
        parsed[r, 1] = content

    return parsed
