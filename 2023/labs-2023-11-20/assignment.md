# select

## reader

Finish the _exercise to the reader_ in [`select/select.c`](https://github.com/devnull-cz/unix-linux-prog-in-c-src/blob/master/select/select.c).

## writer

Q: what happens if non-blocking socket cannot receive any more writes ? (e.g. if the TCP window is full or reduced by the other side).
Try with a sequence of small or singular large buffer.

You can use the example in 
[`select/write-select.c`](https://github.com/devnull-cz/unix-linux-prog-in-c-src/blob/master/select/write-select.c).
as a basis.

# POSIX semaphores

- do not use our code in the labs repo
- run multiple processes, all synchronizing with the same POSIX semaphore set
  with the n=1 (== binary semaphore)
- each process tries to lock using the semaphore
  - when locked, picks a random number of seconds, and each second prints
    out its PID to the **standard error** output
- you should print helpful debugging messages
- test with multiple processes, each started from the same terminal.  Only one
  should be writing at every single moment.

# `shlock`

- implement `shlock` or its subset.  See https://linux.die.net/man/1/shlock
