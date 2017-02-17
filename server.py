#!/usr/bin/env python3

from mongoengine.connection import connect, disconnect
from mongoengine.document import Document
from mongoengine.fields import DateTimeField, IntField, StringField, URLField


class Post(Document):
    ''' Class for defining structure of reddit-top-posts collection
    '''
    url = URLField(required=True)
    date = DateTimeField(required=True)
    commentsUrl = URLField(required=True)
    sub = StringField(max_length=20, required=True) # subredit can be 20 chars
    title = StringField(max_length=300, required=True) # title can be 300 chars
    score = IntField(required=True)

    meta = {
        'collection': 'top_reddit_posts', # collection name
        'ordering': ['-score'], # default ordering
        'auto_create_index': False, # MongoEngine will not create index
        }


if __name__ == "__main__":
    # connect to db
    MONGO_URI = 'mongodb://localhost:27017'
    connect('sivji-sandbox', host=MONGO_URI)

    ## get the last date the webscraper was run
    for post in Post.objects().fields(date=1).order_by('-date').limit(1):
        day_to_pull = post.date.date()

    ## for each distinct subreddit in the last run, print top posts by sub
    for selected_sub in Post.objects(date__gte=day_to_pull).distinct('sub'):

        # formatting
        print('=' * len(selected_sub))
        print(selected_sub)
        print('-' * len(selected_sub))

        # print each post
        for post in Post.objects(date__gte=day_to_pull, sub=selected_sub):
            print('{} - {}'.format(int(post.score), post.title))
        print()
