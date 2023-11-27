## a simple example on threads

- `./a.out <n>`
- allocate array of `n` integer elements in `main`
- create `n` threads
- each thread will get an address of its array element
- each thread will generate a random number to that location
- the main thread joins all the threads, then sorts the array via `qsort`
- `main` prints out the sorted array and exits
- use debug messages to make sure you got everything right

Note that given that each thread will get its own array element to store the
random number to, there is no need to sychronize (that API will be in the next
lecture anyway).

## threaded server

Implement multi-threaded HTTP 1.0 server with `GET` support for static files. 
Use a new thread for every accepted connection.
Choose a document root and serve the files within. Implement basic status codes (200, 404) for the responses.

Use Apache benchmark `ab(1)` (delivered via the `apache2-utils` package on Ubuntu) 
with options `-c` and `-n` to verify it works correctly.

You can reuse existing TCP code from the [src repo](https://github.com/devnull-cz/unix-linux-prog-in-c-src).

## GNU pth thread library

Download the source code from https://www.gnu.org/software/pth/, compile it, ale
link it to your source code using pthread API.

Verify the library is really used (on Linux though, it should be easy as gcc
will not automatically link against a pthread library).

That is, you will not do `gcc -pthread` but rather something like `gcc -L. -R.
-lpth ...`.  See the lecture materials, section on the dynamic linker.

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
