# Tasks for NSWI095 labs, Nov 21, 2022

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
- your solution may first read/write all the input data to the pipe in main(),
  and only then it may start reading the data from the other end.  That is, you
  may assume the data file size is not larger than the sum of all the pipes
  (otherwise main() would put itself to sleep on a full pipe).

```
$ cat /etc/passwd | ./a.out 10 > mypasswd
$ diff -u /etc/passwd mypasswd
$ echo $?
0
```

## `shlock`

- implement `shlock` or its subset.  See https://linux.die.net/man/1/shlock
