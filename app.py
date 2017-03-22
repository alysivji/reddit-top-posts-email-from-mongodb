#!/usr/bin/env python3

"""Script to pull and email last Reddit scape from MongoDB
"""

from top_post_emailer import email_last_scraped_date

if __name__ == '__main__':
    email_last_scraped_date()
