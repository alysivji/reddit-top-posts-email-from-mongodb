#!/usr/bin/env python3

import os
import jinja2

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
    path = os.path.dirname(os.path.abspath(__file__))
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

# THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# def print_html_doc():
#     # Create the jinja2 environment.
#     # Notice the use of trim_blocks, which greatly helps control whitespace.
#     j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
#                          trim_blocks=True)
#     print j2_env.get_template('test_template.html').render(
#         title='Hellow Gist from GutHub'
#     )

# if __name__ == '__main__':
#     print_html_doc()

