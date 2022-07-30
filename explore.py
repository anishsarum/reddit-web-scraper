from pymongo import MongoClient

client = MongoClient(port=27017)
db = client.posts

def queryEngine(attribute = None, value = None):
    if attribute and value:
        query = db.posts.find({attribute: value})
    else:
        query = db.posts.find()

    for post in query:
        print('Title:', post['title'])
        print('Upvotes:', post['upvotes'])
        print('Subreddit:', post['subreddit'])
        print('URL:', post['url'])
        print('')