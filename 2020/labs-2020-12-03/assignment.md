# Tasks for NSWI095 labs, Dec 3, 2020

## `select`

Use `select` to deal with multiple TCP connections in parallel and see if you
can use Apache `ab(1)` with options `-c` and `-n` to verify it works correctly.
You might need to act as an web server to a certain level (e.g. return a simple
HTML page).

Hint: use `telnet webserver-name 80` and type `GET /`

## `poll`

Rewrite
https://github.com/devnull-cz/unix-linux-prog-in-c-src/blob/master/select/select.c
using the `poll` call.

## threaded server

Do the same thing as with the 1st assignment but instead of `select`, use a new
thread for every accepted connection.

## GNU pth thread library

Download the source code from https://www.gnu.org/software/pth/, compile it, ale
link it to your source code using pthread API.

Verify the library is really used (on Linux though, it should be easy as gcc
will not automatically link against a pthread library).
