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
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)
