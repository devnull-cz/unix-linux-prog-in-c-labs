## a simple example on threads

- `./a.out <n>`
- allocate array of `n` integer elements in `main`
- create `n` threads
- each thread will get an address of its array element
- each thread will generate a random number to that location
  - use e.g. `getrandom()`, maybe even with the true-randomnes flag
- the main thread joins all the threads, then sorts the array via `qsort()` (from libc)
- `main` prints out the sorted array and exits
- use debug messages to make sure you got everything right

Note that given that each thread will get its own array element to store the
random number to, there is no need to sychronize (that API will be in the next
lecture anyway).

## multi-threaded HTTP 1.0 server

Implement multi-threaded HTTP 1.0 server (RFC 1945) with `GET` support for static plaintext files 
(i.e. the `Content-type: text/plain` header will be sent). Assume correctly formed requests.

Use a new thread for every accepted connection. Make sure the main thread (or any thread) does not have to join the finished threads.
Choose a document root and serve the files within. Implement basic status codes (200, 404) for the responses.

Using blocking file descriptors throughout the code is fine.

Use `curl`/`wget` for simple functional test. For the former you can use the `--http1.0` command line option to issue HTTP 1.0 request.

Use Apache benchmark `ab(1)` (delivered via the `apache2-utils` package on Ubuntu) 
with options `-c` and `-n` to verify it works correctly.

Consider thread stack size limit w.r.t. the buffer used in the worker threads for the read/write loop.

You can reuse existing TCP code from the [src repo](https://github.com/devnull-cz/unix-linux-prog-in-c-src).

Once you have the skeleton of the server working in basic mode, you can play around with various ways
how to send the file data to the clients, i.e. from the classic open/read/write/close to memory mapped files
and then maybe to `sendfile()`.

## GNU pth thread library

Download the source code from https://www.gnu.org/software/pth/, compile it, ale
link it to your source code using pthread API.

Verify the library is really used (on Linux though, it should be easy as gcc
will not automatically link against a pthread library).

That is, you will not do `gcc -pthread` but rather something like `gcc -lpth ...`. 
See the lecture materials, section on the dynamic linker.

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

# benchmark various IPC

Compare the localhost performance (data passing) of:
  - AF_UNIX socket
  - AF_INET/AF_INET6 socket
  - pipe (unnamed)
  - POSIX MQ
