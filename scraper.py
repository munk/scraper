import requests
from keys import consumer_key, code, access_token
from functools import partial
from bs4 import BeautifulSoup

def get_front_page():
    target = "https://news.ycombinator.com"
    frontpage = requests.get(target)
    if not frontpage.ok:
        raise RuntimeError("Can't access hacker news, you should go outside")
    news_soup = BeautifulSoup(frontpage.text)
    return news_soup


def pocket_auth(consumer_key, auth_code):
    target = 'https://getpocket.com/v3/oauth/authorize'
    request_params = {'consumer_key': consumer_key, 'code': auth_code}
    result = requests.post(target, data=request_params)
    if not result.ok:
        raise RuntimeError("Failed to authenticate!")
    
    return {k: v for k, v in map(lambda s: s.split('='), auth.text.split('&'))}


def add_to_pocket(consumer_key, access_token, url):
    target = 'https://getpocket.com/v3/add'
    request_params = {'url': url, 'consumer_key': consumer_key, 'access_token': access_token}
    result = requests.post(target, data=request_params)
    if not result.ok:
        raise RuntimeError('Failed to post link!')

    return result.text


def find_interesting_links(soup):
    items = soup.findAll('td', {'align': 'right', 'class': 'title'}) 
    links = []
    for i in items:
        try:
            siblings = list(i.next_siblings)
            post_id  = siblings[0].find('a').attrs['id'][3:]
            link     = siblings[1].find('a').attrs['href']
            title    = siblings[1].text
            score    = int(soup.find('span', {'id': 'score_' + post_id}).text.split()[0])
            comments = int(soup.find('a', {'href': 'item?id=' + post_id}).text.split()[0])
        except Exception as e:
            continue
        if 'python' in title.lower() or (score > 50 and comments > 10):
            links.append({'link': link, 'title': title, 'score': score, 'comments': comments})
    return links


if __name__ == '__main__':
    soup = get_front_page()
    pocket = partial(add_to_pocket, consumer_key, access_token)
    results = find_interesting_links(soup)
    for r in results:
        print(pocket(r['link']) )
