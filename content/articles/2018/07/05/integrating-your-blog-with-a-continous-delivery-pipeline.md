Title: Deploying your Blog using a Continous Delivery Pipeline!
Date: 2018-07-15 22:48
Category: Technology
Status: draft
Tags: CI/CD, Travis
Lang: en

I started this blog as Wordpress blog. By that time, I thought I could just use some of the features
that these blog engines provide so I would just focus on writing content. In the beginning that was
true, but I realised that Wordpress was "too heavy" for my purpose. I didn't want to take care of a
database, search for plugins or automate backups (although I liked the automation part of it ;]). That was when a friend at work (thanks [Jesstern](http://jsstrn.me/)) reminded me that I could use static content generators. I liked the idea. As an engineer, I could easily track everything using Git, no databases required,
and I could have everything ready to deploy on my production server using a continous delivery pipeline every commit.

## 1. Setting up the service
Well, I started by choosing the CI service. At first, I thought I could host on my server, but then I realised I didn't want to worry about that right now.
So I ended up going with [TravisCI](http://travis-ci.org): popular service, lots of features and easy to use.
On their [docs](https://docs.travis-ci.com/user/getting-started/#To-get-started-with-Travis-CI), there is a session explaining how to get started with the service.
I recommend you to go over the topics there if you haven't.

## 2. Configuring TravisCI basic structure
```
Travis works by reading a `.travis.yml` file that will be inside your repository.
Make sure to have properly configured your Travis account integration with Github. The link on the previous session explains more about it.
```

After some reading, I added the .travis.yml file to the repository, it looked like this:

    :::yaml
    language: python
    python:
    - '3.6'
    install: pip install -r requirements.txt
    script: make publish

Very simple, right? Every time a commit from now on, Travis will automatically pick my changes and build my project. As you can see, this yaml tells Travis to install
a base structure for a python application (version 3.6), install all the dependencies of my application using pip and finally to use the `script` tag
to run the `make publish` command to build my blog.

### 2.1 Deploying to the VPS
Nice, at this point the blog was building fine, but I wanted more! I wanted Travis to deploy to my production server every commit to my repository.

* Create a new ssh key pair for Travis
* Add the public key to the VPS so Travis can connect
* Encrypt the private key using Travis CLI
* Configure the deploy job on travis to decrypt and use the key during deployment step
