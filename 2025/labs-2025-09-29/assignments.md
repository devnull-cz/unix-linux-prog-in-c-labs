# Intro

- usual compiler options ?
  - `-Wall -Wextra`
  - `-std=c99`

- not so usual but handy
  - sanitizers (address, thread)
  - static analyzers (built-in sometimes)
  - dynamic analyzers (Valgrind)
  - test frameworks

- always check return values and react appropriately
  - `malloc()` (and anything the uses it under the hood) can fail
    - see point 53 on https://www.netmeister.org/blog/cs-falsehoods.html


## Misc

- demonstrate how to use Github + Github actions

1. In you repository, create source code file called `foo.c`
1. In your repository, create file `.github/workflows/build.yml` (basename does not matter) with the following content:
```yaml
name: Build

on:
  push:
    paths-ignore:
    - README.md
  schedule:
  - cron: "0 0 * * 0"

jobs:
  build:
    name: ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest]
    steps:
    - name: Checkout master branch
      uses: actions/checkout@v4
    - name: build
      run: gcc foo.c
    - name: run
      run: ./a.out
```

This will make Github Actions run the sequence of tasks for each item in the matrix on push (and also weekly based on the `cron` schedule), 
in this case on Ubuntu and macOS. This can be further parametrized, e.g. for various compiler implementations/versions.

# Tasks

## Trivia

- see `twenty.c`, find why exactly it does not work and find a fix
- what does the `plus-deref-plus-argv.c` do exactly ?
- ditto for https://github.com/devnull-cz/c-prog-lang/blob/master/src/whole-array.c

Think about the program first, only then run it. Does the runtime match your expectations ?

## Write a program that..

- will define a `void` pointer to self
  - verify that this is the case via debugger (or debug prints)

- prints program arguments (including the name of the program itself),
  each on separate line, using at least 2 ways
  - certainly 3 ways are possible..
    - so you will end up with 3 programs
  - did you use square brackets to access the arguments ?
    - try without them. and without local variables or argument count.

- will print 2nd character of second argument (you can assume there is one), that is `argv[1]`
  of the program in upper case
  - use only pointer arithmetics to do that in single expression
  - now try to write the program with as few characters as possible (you do not have to print the new line)
    - do not modify `argv`
    - https://www.ioccc.org/
    - how many characters does the program have in total ?

- displays an indication by rotating dash/slash/etc. characters
  - printing `\r` will clean the line and revert back to beginning
  - need to `fflush()` the output buffer after each character
  - to sleep under one second use `poll(NUll, 0, <value_in_msec>);`
    - or use usleep(3) (deprecated by POSIX but oh well) or nanosleep(3) 

- will display a moving star (`*`) that is going back and forth on the same line
  - use a reasonable hard coded line length

- will detect if the system is little/big endian machine
  - use only basic C (no system/library calls besides `printf()`)
  - there are multiple ways to do it
  - use `assert()` to make sure the type sizes are what you expect

- implements linked list
  - fill the list with program arguments
  - traverse the list and print each item to separate line
  - free the whole list
    - any memory leaks ?
      - use e.g. Valgrind to check
  - any refactoring yet ?
  - now reimplement using `queue.h` macros (see queue(3) man page)

- will print (to stdout) only the penultimate line of input received on stdin
  - use getline(3)
  - be conservative in memory usage, use `malloc()`/`free()` to allocate the memory
    - hint: array of 2 pointers, `strdup()`
  - exit with error in case of invalid input (at least 2 lines are required)
  - written test cases ?
    - see https://github.com/devnull-cz/stef
      - also remember Github actions (e.g. to automatically run the tests for each integration)

- implement the `strsep(3)` library function
