#!/usr/bin/env python

import os
from jinja2 import Template

template = """Title: {{ title }}
Date: {{ date }}
Category: {{ category }}
Slug: {{ slug }}
Tags: {{ tags}}
Lang: {{ lang }}

Some initial paragraph. Make sure this is not too long so it can fit in the
landing page

## Some topic?
A topic to talk about

## Some code example
```python
import os

path = "content/articles/{}".format(date)
if not os.path.exists(path):
    os.makedirs(path)
print(path)
```

## This is how to include a image
![Workstation]({filename}/articles/2018/03/18/canada-workstation.png)
*My workstation in Canada (2014/2015)*
"""

title = input("Title: ")
date = input("Date: ")
category = input("Category: ")
slug = input("Slug: ")
tags = input("Tags: ")
lang = input("Lang: ")

j2 = Template(template)
output = j2.render(title=title, date=date, category=category, slug=slug, tags=tags, lang=lang)

path = "content/articles/{}".format(date)
if not os.path.exists(path):
    os.makedirs(path)

filename = slug + ".md"
with open(os.path.join(path,filename), "w") as file:
    file.write(output)

