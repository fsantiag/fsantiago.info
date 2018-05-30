#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Felipe Santiago'
SITENAME = 'fsantiago.info'
SITEURL = ''
SITESUBTITLE= 'Techonology, living experiences and gaming smashed together!'

THEME = 'themes/hyde'

PATH = 'content'
#STATIC_PATHS = ['2018-03-18']
#ARTICLE_PATHS = ['2018-03-18']

TIMEZONE = 'Asia/Singapore'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('github', 'https://github.com/fsantiag/'),
        ('linkedin', 'https://www.linkedin.com/in/felipe-santiago'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
