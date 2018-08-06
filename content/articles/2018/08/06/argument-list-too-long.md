Title: Error: Argument list too long
Date: 2018-08-06 21:34
Category: Technology
Tags: Linux, Bash, Ansible, Error
Lang: en

Today I faced an unsual error. One of the jobs in the CI server was failing with the following message: `[Argument list too long]`.
After some debugging and reading, I figured that the error is related to a kernel limitation, apparently well known, and today I am going to explain what I did to fix this.

Everything started with this failing job on our CI server. It suddenly started failing for no reason.  What was also unusual was the error message: `Argument list too long`.

I starded by reading the script that was being executed again. Just to give you some background, we have this set of ansible playbooks that run different kinds of job.
This one in particular, was doing something like this:

```yaml
- name: My great task
  local_action: shell echo "{{ old_var.stdout }}" | sed s/old/new/g
  register: new_variable
```

This block was exactly where we were getting the error. Basically, the variable `old_var` was the output of an API call to a service performed in the previous ansible task.
What they were trying to do was to replace some strings in the response from the service using `sed`. That is the reason why you can see the `echo` followed by the `sed`
command and later the assignment to `new_variable`.

Well, since no changes were actually applied to that part of the code and the job was working fine few days back, I assumed something external was causing the problem.
In this case, the external portion was related to the API response. That was the only thing that could actually change unexpectedly simply because it was not in my control.

I compared the last successful job with the failing one. The API response was a bit bigger in the failing job, which connects with the error message: `Argument list too long`.
At this point I already had something in mind: the API response has more data than before, which causes the command argument to be bigger than expected and therefore, the
command fails because the argument list is indeed too long.

Good, I thought I was on the right track, however I didn't know exactly what was actually causing the problem.
In this case, any of the commands could have some limitation: `sed`, `echo`, or even the pipe itself.

I went on the internet looking for this especific error and I found some interesting results [here](https://linux.die.net/man/2/execve), [here](https://stackoverflow.com/questions/11289551/argument-list-too-long-error-for-rm-cp-mv-commands) and [here](https://www.linuxjournal.com/article/6060).

In those links, I was able to notice this is a kernel limitation on the size of command line arguments. Most of the links were reporting problems when using wildcards in the commands, however the actual problem was not the wildcard itself but the size of the command generated when using the wildcards.
Most UNIX implementations have some limit in the size of a command line argument. That limit can be verified by running the following command:

```
getconf ARG_MAX
```

Finally, we found a proper answer. Now I could fix the problem in peace! ;]

In my case, I decided to write the API response to a temporary file and later run the operations using the file. This way the size of the API response wouldn't matter, since the command would always point to the file. Something similar to this:

```yaml
- name: Write to file
  local_action: copy content={{ old_var.stdout }} dest=/path/to/destination/file

- name: My great task
  local_action: command sed s/old/new/g /path/to/destination/file
  register: new_variable
```

Easy right? That's it for now! Let me know what you think about this solution!

Cheers!
