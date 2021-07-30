import urllib.request
from bs4 import BeautifulSoup

import base64

url = str(input())

html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

# kill all script and style elements
for script in soup(['script', 'style', 'meta', '[document]']):
    script.extract()    # rip it out

# get html tag contents
html = soup.find('html')

#remove all links
for a in soup.findAll():
    del a['href']

#write to file
f = open('op.html', 'w', encoding='utf-8')
b64code = base64.b64encode(bytes(str(html), 'utf-8'))
b64decoded = str(base64.b64decode(b64code), 'utf-8')
f.write(b64decoded)
f.close()