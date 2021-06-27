Title: Handling POSIX signals in bash using trap
Date: 2021/06/27
Category: Technology
Slug: bash-trap
Tags: Linux, POSIX, Signals, Trap, Bash
Lang: en

Bash has a way of intercepting signals to perform actions. This is a nice way to have cleanup functions
that can be executed before the program exists. Here are some examples in how you can setup
a function that is capable of intercepting signals.
```bash
#!/bin/bash
# settting up the trap for the function 'cleanup'. The number 2 here refers to SIGINT signals.
trap cleanup 2
cleanup() {
  echo "Signal intercepted!"
}

sleep 60 &
wait $!
```
As you can imagine, you can specify multiple signals to be handled by the same function:
```bash
trap catch 2 15
```
You can also use the signal codes if you find that more legible:
```bash
trap catch SIGINT SIGTERM
```
Here is a list of some of the common signals:

| Signal Number | Signal Code |
|:-------------:|:-----------:|
| 1             | SIGHUP      |
| 2             | SIGINT      |
| 3             | SIGQUIT     |
| 9             | SIGKILL     |
| 15            | SIGTERM     |