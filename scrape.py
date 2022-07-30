from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

# Get the data from the website.
html_text = requests.get('https://old.reddit.com', headers={'User-Agent': 'Mozilla/5.0'}).text
soup = BeautifulSoup(html_text, 'lxml')
posts = soup.find('div', class_ = 'sitetable linklisting').find_all('div', {'data-context': 'listing'})
results = []

client = MongoClient(port=27017)

db = client.posts
post_count = 1

for post in posts:
    if post['data-promoted'] == 'false':

        # Get all the relevant information required
        title = post.find('a', {'data-event-action': 'title'}).text
        url = post.find('a', {'data-event-action': 'comments'})['href']
        subreddit = post['data-subreddit-prefixed']
        upvotes = post['data-score']

        # Structure the data for entering into the database
        data = {
            'title': title,
            'url': url,
            'subreddit': subreddit,
            'upvotes': upvotes
        }

        # Track progress of importing
        result = db.posts.insert_one(data)
        print('Created {0} of 25 as {1}'.format(post_count, result.inserted_id))
        post_count += 1

        # print(f'Title:     {title}')
        # print(f'Url:       {url}')
        # print(f'Subreddit: {subreddit}')
        # print(f'Upvotes:   {upvotes}')

print('Finished importing 25 reddit posts.')