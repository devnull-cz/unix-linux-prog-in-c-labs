# Intro

# Misc

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

  - write a program that will define a void pointer to self
    - verify that this is the case via debugger (or debug prints)

  - warmup:
    - write a program that will print (to stdout) only penultimate line of input received on stdin
    - use getline(3)
    - be conservative in memory usage, use malloc()/free() to allocate the memory
    - exit with error in case of invalid input (at least 2 lines are required)
    
