# Tasks for NSWI095 labs, Nov 19, 2020

## `shlock`

- implement `shlock` or its subset.  See https://linux.die.net/man/1/shlock

## Signal ping-pong

- make two processes send each other a signal in turns.  Figure out your own
  solution.  Try multiple of those.
- you may use `sleep(1)` if it helps to make it reliable (that is, to avoid
  missed signals).  However, you can also use file locking to avoid any busy
  waiting.

## Use `sigwait`

- use `sigwait` from a process just to wait for signals.  Report all the
  progress.  Send signals to the process from a different terminal to observe.

## Pipe circle

- `./a.out <n>`

- a process creates `<n>` new processes
- from the main process, connect processes via pipes to form a one-way full
  circle
- main process's input is connected to the pipe to the first process
- the data goes through the full circle and what the main process reads from the
  last process is written to its standard output
- make sure you try it out with a file of at least a few megabytes.
- if your process hangs, it means you did not close all unused file descriptors

```
$ cat /etc/passwd | ./a.out 10 > mypasswd
$ diff -u /etc/passwd mypasswd
$ echo $?
0
```
