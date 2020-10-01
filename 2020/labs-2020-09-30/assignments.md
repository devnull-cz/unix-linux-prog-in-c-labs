# Intro

- usual compiler options ?
  - `-Wall -Wextra`
  - `-std=c99`

- always check return values and react appropriately
  - malloc() (and anything the uses it under the hood) can fail
    - see point 53 on https://www.netmeister.org/blog/cs-falsehoods.html


## Misc

- demonstrate how to use Github + Travis/Github actions
  - `.travis.yml` contents:
```yml
  language: c
  compiler:
  - clang
  - gcc
  script: make
```

# Tasks

## Trivia

- see `twenty.c`, find why exactly it does not work and find a fix
- what does the `plus-deref-plus-argv.c` do exactly ?

## Write a program that..

- will define a void pointer to self
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
    - do not modify argv
    - https://www.ioccc.org/
    - how many characters does the program have in total ?

- displays a indication by rotating dash/slash/etc. characters
  - printing `\r` will clean the line and revert back to beginning
  - need to `fflush()` the output buffer after each character
  - to sleep under one second use `poll(NUll, 0, <value_in_msec>);`

- will display a moving star (`*`) that is going back and forth
  - use a reasonable hard coded line length

- will detect if the system is little/big endian machine
  - use only basic C (no system/library calls besides printf())
  - there are multiple ways to do it
  - use assert() to make sure the type sizes are what you expect

- implements linked list
  - fill the list with program arguments
  - traverse the list and print each item to separate line
  - free the whole list
    - any memory leaks ?
  - any refactoring yet ?
  - now reimplement using queue.h macros (see queue(3) man page)

- will print (to stdout) only the penultimate line of input received on stdin
  - use getline(3)
  - be conservative in memory usage, use malloc()/free() to allocate the memory
    - hint: array of 2 pointers, strdup()
  - exit with error in case of invalid input (at least 2 lines are required)
  - written test cases ?
    - see https://github.com/devnull-cz/stef

