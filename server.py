#!/usr/bin/env python3

import os
from mongoengine.connection import connect
from mongoengine.document import Document
from mongoengine.fields import DateTimeField, IntField, StringField, URLField
import jinja2

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

def render(tpl_path, context):
    ''' Given jinja2 template, generate HTML
    Adapted from http://matthiaseisen.com/pp/patterns/p0198/

    Args:
        * tpl_path - template path
        * context - dict of variables to pass in
    '''
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

if __name__ == "__main__":
    # connect to db
    MONGO_URI = 'mongodb://localhost:27017'
    connect('sivji-sandbox', host=MONGO_URI)

    ## get the last date the webscraper was run
    for post in Post.objects().fields(date=1).order_by('-date').limit(1):
        day_to_pull = post.date.date()

    ## pass in variables render template
    context = {
        'day_to_pull': day_to_pull,
        'Post': Post,
    }

    with open("output1.html", 'w') as f:
        html = render("template.html", context)
        f.write(html)
