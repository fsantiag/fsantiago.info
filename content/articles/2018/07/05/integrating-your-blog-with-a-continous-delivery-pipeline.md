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

## 1. Configuring the Continous Delivery Pipeline
Well, I started by choosing the CI service. At first, I thought I could host on my server, but then I realised I didn't want to worry about that right now.
So I ended up going with [TravisCI](http://travis-ci.org): popular service, lots of features and easy to use.
On their [docs](https://docs.travis-ci.com/user/getting-started/#To-get-started-with-Travis-CI), there is a session explaining how to get started with the service.
I recommend you to go over the topics there if you haven't.

After some reading, I added the .travis.yml file to the repository, it looked like this:

    :::yaml
    language: python
    python:
    - '3.6'
    install: pip install -r requirements.txt
    script: make publish

Very simple, right? Every time a commit from now on, Travis will automatically pick my changes and build my project. As you can see, this yaml tells Travis to install
a base structure for a python application (version 3.6), install all the dependencies of my application using pip and finally to run the `make publish` command
to build my blog.

## 2. Automating the VPS deployment
Nice, at this point the blog was building fine, but I wanted more! I wanted Travis to deploy to my production server every single commit. Let's do this!

* Create a new ssh key pair for Travis:

        :::shell
        ssh-keygen -t rsa -b 4096 -C 'build@travis-ci.org' -f ./travis_rsa

Tip: Don't set the password for the key so travis will not be prompted when connecting

* Add the public key to the VPS so Travis can connect

        :::shell
        ssh-copy-id -i deploy_rsa.pub myuser@myhost
    All keys were skipped because they already, use -f

* Encrypt the private key using Travis CLI

        :::shell
        travis encrypt-file deploy_rsa --add

    travis command line will add this to your .travis file

        :::yaml
        before_install:
        - openssl aes-256-cbc -K $encrypted_da7eec2e51b3_key -iv $encrypted_da7eec2e51b3_iv
          -in travis_rsa.enc -out travis_rsa -d

    And will also save the password to decrypt the file as an enviornment variable that only your build job have access
Travis will use before_install, however I prefer before_deploy cause I just want to execute that step in case of deployment.

* Cleanup and push

        :::shell
        rm -f deploy_rsa deploy_rsa.pub
        git add deploy_rsa.enc

* Configure the deploy job on travis to decrypt and use the key during deployment step

By reading the documentation, I saw that we could use after_success to run the deploy however a non zero return code wouldn't break the build, so I decided to use the deploy with a custom script.

        :::shell
        deploy:
          provider: script
          script: bash scripts/deploy.sh
          on:
            branch: develop

When you push the changes, travis will be prompted
```
Are you sure you want to continue connecting (yes/no)?
```
Because it doesn't know the host

        :::shell
        addons:
          ssh_known_hosts: fsantiago.info

Now we are going to be prompted for a password because we didn't add the key to the ssh-agent
Dont forget to start the ssh-agent before, otherwise ssh-add will fail

        :::shell
        before_deploy:
        - openssl aes-256-cbc -K $encrypted_da7eec2e51b3_key -iv $encrypted_da7eec2e51b3_iv
          -in travis_rsa.enc -out /tmp/travis_rsa -d
        - eval "$(ssh-agent -s)"
        - ssh-add /tmp/travis_rsa
