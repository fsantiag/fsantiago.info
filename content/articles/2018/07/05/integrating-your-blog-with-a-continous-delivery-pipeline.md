Title: Deploying your blog using a Continous Delivery Pipeline over SSH
Date: 2018-07-12 22:48
Category: Technology
Tags: CI/CD, Travis CI, SSH, Deployment
Lang: en

I started this blog as a Wordpress blog. By that time, I thought I could just use some of the features that these blog engines provide so
I would just focus on writing content. In the beginning that was true, but I realised that Wordpress was "too heavy" for my purpose.
I didn't want to take care of a database, search for plugins or automate backups (although I liked the automation part of it ;]).
That was when a friend at work (thanks [Jesstern](http://jsstrn.me/)) reminded me that I could use static site generators and I liked the idea. In addition,
I decided to use a delivery pipeline to take my blog to production!

## 1. Setting up the basic structure for the Contrinous Integration service
Well, I started by choosing the CI service. At first, I thought I could host on my server. Later, I realised I didn't want to worry about that right now. Maybe in the
future. That is why I ended up going with [Travis CI](http://travis-ci.org): popular service, lots of features and easy to use.

On their [docs](https://docs.travis-ci.com/user/getting-started/#To-get-started-with-Travis-CI), there is a session explaining how to get started with the service.
I recommend you to go over the topics there if you haven't. It will help you to not feel lost in the next sections as well authorize Travis to connect to your repository.
As a side note, keep in mind that Travis requires you to use Github and it is only free if your project is public.

If you are not familiar with continous integration (or just CI), check out this [article](https://www.thoughtworks.com/continuous-integration) that my employer [ThoughtWorks](https://www.thoughtworks.com/) has published. It is great to have an overview.


```At this point, I am assuming that you already have some blog/website/whatever and you've read the docs that I referenced in the previous paragraph. Regarding this blog, I am using [Pelican](http://docs.getpelican.com/en/stable/) to generate it and that is the reason why you will see an Python environment being setup on Travis.```

After some reading, I added the .travis.yml at the root of repository, similar to this:

    :::yaml
    language: python
    cache: pip
    python:
    - '3.6'
    install: pip install -r requirements.txt
    script: make publish

Very simple, right? As you can see, this yaml tells Travis to install a base structure for a Python application (version 3.6), install all the dependencies of my application using pip and finally to run the *make publish* command to build my blog. That is how Travis will pick every commit and build my project! Oh, I also added the cache tag to prevent downloading dependencies every build!

## 2. Automating the deployment on the Virtual Private Server
Nice, at this point the blog was building fine but I wanted more! I wanted Travis to deploy to my production server on every single commit. Let's do this!

After every build, I needed to copy the files to the server (deploy). Now you might be thinking that I could use a regular *scp* command, however I decided to use [rsync](https://en.wikipedia.org/wiki/Rsync) instead. Rsync is a bit "smarter" when compared to scp. It checks sizes and timestamps and only transfer changes. Cool, isn't it? Good, but to make rsync work, I also needed to configure a ssh key pair so Travis build agent could easily connect to my server. Here is how I broke down the tasks:

### 2.1 Create a new ssh key pair for Travis:

```Tip: Don't set the password for the key or Travis will be prompted during deployment.```

    :::sh
    ssh-keygen -t rsa -b 4096 -C 'build@travis-ci.org' -f ./travis_rsa

### 2.2 Add the public key to the VPS:

This is how we tell the VPS server to allow Travis to connect using the private key.

```Tip: If you get a message saying that all keys were skipped because they were already added, just add the -f (force) option. If you prefer, you can add
 the key manually by inserting in the authorized_keys file under ~/.ssh```

    :::sh
    ssh-copy-id -i travis_rsa.pub <myuser>@<myhost>


### 2.3 Encrypt the private key using Travis CLI:

Travis provides a command line tool to interface with TravisCI service. [Here](https://github.com/travis-ci/travis.rb#installation) you can find
 some installation instructions and this is the command we can run:

    :::sh
    travis encrypt-file travis_rsa --add

If successful, this command will add the following to your .travis.yml:

    :::yaml
    before_install:
    - openssl aes-256-cbc -K $encrypted_****_key -iv $encrypted_****_iv
      -in travis_rsa.enc -out /tmp/travis_rsa -d

and also save the password to decrypt the file as an environment variable that only your build job have access.

```Tip: Travis will add the before_install tag, however I noticed that I wanted this step to execute only in case of deployment, so I replaced
it with the before_deploy.```

```Tip: I extracted my key in the /tmp folder just to make sure I would not copy it by mistake to a wrong place. Once the job finishes, the key would be completely gone.```

### 2.4 Configure the deployment job:

I saw that we could use `after_success` tag to run the deploy, however, a non zero return
code would [NOT](https://docs.travis-ci.com/user/customizing-the-build/#Breaking-the-Build) break the build. So, I decided to use the `deploy` tag
with a  custom script. I also added the **skip_cleanup** tag that would prevent travis from resetting my working directory and deleting all files generated
during the build.

    :::yaml
    deploy:
      provider: script
      skip_cleanup: true
      script: rsync -r --delete-before --quiet $TRAVIS_BUILD_DIR/output/* fsantiago@fsantiago.info:/home/fsantiago/fsantiago.info/content
      on:
        branch: master

Here I especifically mentioned to only deploy if we are working on the master branch. That is why the `before_deploy` tag I mentioned earlier
also makes sense. If I ever push changes to a branch, my blog would build but no deployment would be executed. If we are not deploying, no need
for decrypting the key, right?

The `script` tag executes the rsync command that will actually copy the files to server. The files are copied straight to the web server folder.

Make sure to also add your VPS host as a known host to prevent being asked to add the fingerprint during deployment using the following:

    :::yaml
    addons:
      ssh_known_hosts: <myhost>

At this point, if we push the changes and observe what Travis would do, you will see that we will be prompted for a password.
That is expected because we are not using the SSH key yet! We added a line to decrypt the key, but we haven't actually added the key to the ssh-agent. Therefore,
the rsync command actually tries to use password authentication. Let's fix that now.

Oh, we can't forget to start the ssh-agent before and set the right permission to the key file, otherwise ssh-add will fail:

    :::shell
    before_deploy:
    - openssl aes-256-cbc -K $encrypted_****_key -iv $encrypted_****_iv
      -in travis_rsa.enc -out /tmp/travis_rsa -d
    - eval "$(ssh-agent -s)"
    - ssh-add /tmp/travis_rsa

### 2.5 Cleanup:

Last but not least, make sure to delete the keys and only push the encrypted file!

    :::shell
    rm -f travis_rsa travis_rsa.pub
    git add travis_rsa.enc


Awesome! That is it! We are now able to use continous deployment to take our blog to production any time! Of course, my blog is very small and this is
probably an overkill solution, however I focused on practicing/learning and I hope you could find it useful too. I am using Travis CI and Github to store and deploy my blog, however you could use the same approach with any other CI tool. If you have any questions/feedback, leave a comment
 or drop me an email! I will be happy to get in touch!
