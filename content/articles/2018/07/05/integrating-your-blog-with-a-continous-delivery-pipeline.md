Title: Integrating your blog with a Continous Delivery Pipeline!
Date: 2018-07-15 22:48
Category: Technology
Status: draft
Tags: foo
Lang: en

I started this blog as Wordpress blog. By that time, I thought I could just use some of the features
that these blog engines provide so I would just focus on writing content. In the beginning that was
true, but I realised that Wordpress was "too heavy" for my purpose. I didn't want to take care of a
database, search for plugins or automate backups (although I liked the automation part of it ;)). That was when a friend at work reminded me that I
could use static content generators. I liked the idea. As an engineer, I could easily track everything using Git, no databases required,
and I could also apply continous deployment to make every commit go straight to my production server.

    :::python
    import os
    def my_method(something):
        my_dict = {}
        my_list = ["1", "2", "3"]
        os.do_something("lol")
        return "foo"

Fumex

    :::go
    func main() {

        // Create our Temp File
        tmpFile, err := ioutil.TempFile(os.TempDir(), "prefix-")
        if err != nil {
            log.Fatal("Cannot create temporary file", err)
        }

        fmt.Println("Created File: " + tmpFile.Name())

        // Example writing to the file
        _, err = tmpFile.Write([]byte("This is a golangcode.com example!"))
        if err != nil {
            log.Fatal("Failed to write to temporary file", err)
        }

        // Remember to clean up the file afterwards
        defer os.Remove(tmpFile.Name())
    }

Testing
```foo
This is how I highlight a <b>text</b>
```

