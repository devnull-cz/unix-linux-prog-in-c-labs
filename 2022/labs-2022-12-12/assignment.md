# Tasks for NSWI095 labs, Dec 12, 2022

## `select`

Use `select` to deal with multiple TCP connections in parallel and see if you
can use Apache `ab(1)` with options `-c` and `-n` to verify it works correctly.
You might need to act as an web server to a certain level (e.g. return a simple
HTML page).

Hint: use `telnet webserver-name 80` and type `GET /`

You can so use `nc` for debugging:

```
nc -l -p 8080 127.0.0.1
```

And form another terminal:

```
ab http://127.0.0.1:8080/
```

## `poll`

Rewrite
https://github.com/devnull-cz/unix-linux-prog-in-c-src/blob/master/select/select.c
using the `poll` call.

## a simple example on threads

- `./a.out <n>`
- allocate array of `n` elements in `main`
- create `n` threads
- each thread will get an address of its array element
- each thread will generate a random number to that location
- the main thread joins all the threads, then sorts the array via `qsort`
- `main` prints out the sorted array and exits
- use debug messages to make sure you got everything right

Note that given that each thread will get its own array element to store the
random number to, there is no need to sychronize (that API will be on next
lecture anyway).

## threaded server

Do the same thing as with the 1st assignment but instead of `select`, use a new
thread for every accepted connection.

Alternatively, as a simpler task, take some existing TCP code from our repo and
create a new thread for each accepted connection, and just write the data on the
standard output.  Verify it works correctly.

## GNU pth thread library

Download the source code from https://www.gnu.org/software/pth/, compile it, ale
link it to your source code using pthread API.

Verify the library is really used (on Linux though, it should be easy as gcc
will not automatically link against a pthread library).

That is, you will not do `gcc -pthread` but rather something like `gcc -L. -R.
-lpth ...`.  See the lecture materials, section on the dynamic linker.
