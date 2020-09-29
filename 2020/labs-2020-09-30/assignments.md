# Intro

- usual compiler options ?
  - `-Wall -Wextra`
  - `std=c99`

- always check return values and react appropriately
  - malloc() (and anything the uses it under the hood) can fail
    - see point 53 on https://www.netmeister.org/blog/cs-falsehoods.html


## Misc

- demonstrate how to use Github+Travis
  - `.travis.yml` contents:
```yml
  language: c
  compiler:
  - clang
  - gcc
  script: make
```

# Tasks

## Write a program that..

- will define a void pointer to self
  - verify that this is the case via debugger (or debug prints)
  - use assert() to make sure the type sizes are what you expect

- prints program arguments, each on separate line, using at least 2 ways
  - certainly 3 ways are possible..

- will print 2nd character of second argument (assuming there is one)
  of the program in upper case
  - use only pointer arithmetics to do that in single expression

- will detect if the system is little/big endian machine
  - use only basic C (no system/library calls besides printf())
  - there are multiple ways to do it

- will implement linked list
  - fill the list with program arguments
  - traverse the list and print each item to separate line
  - free the whole list
    - any memory leaks ?
  - now reimplement using queue.h macros (see queue(3) man page)

- will print (to stdout) only the penultimate line of input received on stdin
  - use getline(3)
  - be conservative in memory usage, use malloc()/free() to allocate the memory
    - hint: array of 2 pointers, strdup()
  - exit with error in case of invalid input (at least 2 lines are required)
