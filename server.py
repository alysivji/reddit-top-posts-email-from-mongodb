#!/usr/bin/env python3

import os
from mongoengine.connection import connect
from mongoengine.document import Document
from mongoengine.fields import DateTimeField, IntField, StringField, URLField
from jinja2 import Environment, FileSystemLoader

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

## jinja variables
PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    ## add template directory
    loader=FileSystemLoader(os.path.join(PATH, '')),
    trim_blocks=False)

def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

if __name__ == "__main__":
    # connect to db
    MONGO_URI = 'mongodb://localhost:27017'
    connect('sivji-sandbox', host=MONGO_URI)

    ## get the last date the webscraper was run
    for post in Post.objects().fields(date=1).order_by('-date').limit(1):
        day_to_pull = post.date.date()

    ## render template (set vars)
    fname = "output.html"
    context = {
        'day_to_pull': day_to_pull,
        'Post': Post,
    }

    ## render template (write file)
    with open(fname, 'w') as f:
        html = render_template('template.html', context)
        f.write(html)
