#!/usr/bin/env python3

import os
import configparser
from mongoengine.connection import connect
from mongoengine.document import Document
from mongoengine.fields import DateTimeField, IntField, StringField, URLField
import jinja2
import requests
from requests.exceptions import HTTPError


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
        * tpl_path - jinja2 template path
        * context - dict of variables to pass in

    Returns:
        * rendered HTML from jinja2 templating engine
    '''
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

def send_email(html):
    '''Given HTML template, sends Reddit Top Post Digest email using MailGun's API

    Arg:
        html - HTML to send via email

    Returns:
        None
    '''
    ## api params (using configparser)
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    key = config.get('MailGun', 'api')
    domain = config.get('MailGun', 'domain')

    ## set requests params
    request_url = 'https://api.mailgun.net/v3/{0}/messages'.format(domain)
    payload = {
        'from': 'alysivji@gmail.com',
        'to': 'alysivji@gmail.com',
        'subject': 'Reddit Top Post Digest',
        'html': html,
    }

    try:
        r = requests.post(request_url, auth=('api', key), data=payload)
        r.raise_for_status()
        print('Success!')
    except HTTPError as e:
        print('Error {}'.format(e.response.status_code))


if __name__ == "__main__":
    # connect to db
    MONGO_URI = 'mongodb://localhost:27017'
    connect('sivji-sandbox', host=MONGO_URI)

    ## get the last date the webscraper was run
    for post in Post.objects().fields(date=1).order_by('-date').limit(1):
        day_to_pull = post.date.date()

    ## pass in variables, render template, and send
    context = {
        'day_to_pull': day_to_pull,
        'Post': Post,
    }
    html = render("template.html", context)
    send_email(html)
