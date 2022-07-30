from bs4 import BeautifulSoup
import requests
import time

html_text = requests.get('https://old.reddit.com', headers={'User-Agent': 'Mozilla/5.0'}).text
soup = BeautifulSoup(html_text, 'lxml')
posts = soup.find('div', class_ = 'sitetable linklisting').find_all('div', {'data-context': 'listing'})

for post in posts:
    if post['data-promoted'] == 'false':
        title = post.find('a', {'data-event-action': 'title'}).text
        subreddit = post['data-subreddit-prefixed']
        upvotes = post['data-score']

        print(f'Title:     {title}')
        print(f'Subreddit: {subreddit}')
        print(f'Upvotes:   {upvotes}')
        print('')