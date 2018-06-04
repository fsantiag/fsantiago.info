#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Felipe Santiago'
SITENAME = 'Felipe Santiago'
SITEURL = 'localhost'
DISQUS_SITENAME = 'fsantiago-info'
SITESUBTITLE= 'Techonology, living experiences and gaming smashed together!'

# This is here to allow static files be placed with md files
STATIC_PATHS=['articles', 'images']
ARTICLE_PATHS=['articles']
ARTICLE_URL = 'articles/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_SAVE_AS = 'articles/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'

THEME = 'themes/hyde'

PATH = 'content'

TIMEZONE = 'Asia/Singapore'

RELATIVE_URLS= True

PROFILE_IMAGE = 'myself.jpg'
# DEFAULT_LANG = 'en'

# Social widget
SOCIAL = (('github', 'https://github.com/fsantiag/'),
        ('linkedin', 'https://www.linkedin.com/in/felipe-santiago'),)

DEFAULT_PAGINATION = False
