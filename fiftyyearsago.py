import requests
import datetime
from bs4 import BeautifulSoup

today = datetime.date.today()
url = 'http://en.wikipedia.org/wiki/' + today.strftime('%B') + '_' + str(today.year - 50)
target = today.strftime('%B') + '_' + str(today.day) + '.'

data = requests.get(url).text
soup = BeautifulSoup(data)

contents = soup.find('div', {'id': 'toc'})
a = contents.findAll('a')

todaytag = filter(lambda tag: target in tag.attrs.get('id', []), soup.findAll('span'))[0]
events = todaytag.find_next('ul')

for event in events.findAll('li'):
    print(event.text)
