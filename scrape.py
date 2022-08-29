from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

# Get the data from the website.
html_text = requests.get('https://old.reddit.com', headers={'User-Agent': 'Mozilla/5.0'}).text
soup = BeautifulSoup(html_text, 'lxml')
posts = soup.find('div', class_ = 'sitetable linklisting').find_all('div', {'data-context': 'listing'})
results = []

# Use standard port 27017 for MongoDB.
client = MongoClient(port=27017)

db = client.posts
post_count = 1

for post in posts:
    if post['data-promoted'] == 'false':

        # Get all the relevant information required.
        title = post.find('a', {'data-event-action': 'title'}).text
        url = post.find('a', {'data-event-action': 'comments'})['href']
        subreddit = post['data-subreddit-prefixed']
        upvotes = post['data-score']

        # Structure the data for entering into the database.
        data = {
            'title': title,
            'url': url,
            'subreddit': subreddit,
            'upvotes': upvotes
        }

        # Update entry if article with same title is already in database.
        if db.posts.find_one({'title': title}):
            result = db.posts.find_one_and_update({'title': title}, {'$set': {'upvotes': upvotes}})
            print(f'Updated {post_count} of 25 as {result}')
        else:
            result = db.posts.insert_one(data)
            print(f'Created {post_count} of 25 as {result.inserted_id}')

        # Track progress of importing.
        post_count += 1

print('Finished importing 25 reddit posts.')