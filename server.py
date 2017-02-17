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

    for post in Post.objects():
        print('{} - {}'.format(int(post.score), post.title))
