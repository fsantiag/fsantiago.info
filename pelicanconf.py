#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Felipe Santiago'
SITENAME = 'fsantiago.info'
SITEURL = 'http://fsantiago.info'
SITESUBTITLE= 'Techonology, living experiences and gaming smashed together!'

THEME = 'themes/hyde'

PATH = 'content'
#STATIC_PATHS = ['2018-03-18']
#ARTICLE_PATHS = ['2018-03-18']

TIMEZONE = 'Asia/Singapore'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

# Social widget
SOCIAL = (('github', 'https://github.com/fsantiag/'),
        ('linkedin', 'https://www.linkedin.com/in/felipe-santiago'),)

DEFAULT_PAGINATION = False
