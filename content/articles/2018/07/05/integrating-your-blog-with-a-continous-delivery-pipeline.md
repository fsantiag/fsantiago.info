Title: Deploying your Blog using a Continous Delivery Pipeline!
Date: 2018-07-15 22:48
Category: Technology
Status: draft
Tags: CI, CD, Travis
Lang: en

I started this blog as Wordpress blog. By that time, I thought I could just use some of the features
that these blog engines provide so I would just focus on writing content. In the beginning that was
true, but I realised that Wordpress was "too heavy" for my purpose. I didn't want to take care of a
database, search for plugins or automate backups (although I liked the automation part of it ;]). That was when a friend at work (thanks [Jesstern](http://jsstrn.me/)) reminded me that I
could use static content generators. I liked the idea. As an engineer, I could easily track everything using Git, no databases required,
and I could have everything ready to deploy on my production server using a continous delivery pipeline every commit.

## 1. Setting up the Continous Integration service
Well, I started by choosing the CI service. At first, I thought I could host on my server, but then I realised I didn't want to worry about that right now.
So I ended up going with [TravisCI](http://travis-ci.org): popular service, lots of features and easy to use.i
On their [docs](https://docs.travis-ci.com/user/getting-started/#To-get-started-with-Travis-CI), there is a session explaining how to get started with the service. I recommend you to go over if you haven't before diving into the next session.

### 1.1 Configuring the yml file
Travis works by reading a `.travis.yml` file that will be inside your repository. You can find more about their file structure by reading their docs on the link
I referenced before.
Your .travis.yml file will look like this in the first moment:

    :::yaml
    language: python
    python:
    - '3.6'
    install: pip install -r requirements.txt
    script: make publish

Ok, that is great! If you make a small commit now, Travis will automatically pick your changes and build your project. As you can tell, the `script` tag
executes the `make publish` command to build my blog. Check your Travis account to see how is the state of your build.

