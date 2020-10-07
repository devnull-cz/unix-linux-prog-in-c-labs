# Linker and libraries

- write two libraries, `liba` and `libb`, and a program `main.c`
- `liba` will define a function `fna` which calls a function `fnb`
- function `fnb` will be defined in `libb`
- design `fna` and `fnb` as you wish just make sure they return something based
  on argv[1], and print that out from `main`
- `main()` from `main.c` only calls function `fna`
- make sure you can call the program from a local directory as `./a.out`, and
  also from the `/` directory using a full path.

# Makefile
- write a makefile for the previous task
- use `touch(1)` to verify you only rebuild what is necessary and nothing else

# Environment

- write a simple env(1) program
  - `env [-] [varname=value [varname=value ...]] command`
  - if the first argument is `-`, clear the environment before executing the
    command
  - set environment variables in the caller if present on the command line
  - to execute the command, use `system(3)`
  - all other arguments aside from the last one are variable definitions
  - do a reasonable error checking

Example:

```
$ ./a.out - HELLO=hello LOCO=loco env
PWD=/afs/ms.mff.cuni.cz/u/p/pechanec
HELLO=hello
SHLVL=0
LOCO=loco
_=/usr/bin/env

$ ./a.out date
Wed Oct  7 11:28:20 PM CEST 2020

$ ./a.out LD_DEBUG=help ldd
Valid options for the LD_DEBUG environment variable are:

  libs        display library search paths
  reloc       display relocation processing
  files       display progress for input file
  symbols     display symbol table processing
  bindings    display information about symbol binding
  versions    display version dependencies
  scopes      display scope information
  all         all previous options combined
  statistics  display relocation statistics
  unused      determined unused DSOs
  help        display this help message and exit

To direct the debugging output into a file instead of standard output
a filename can be specified using the LD_DEBUG_OUTPUT environment variable.

$ ./a.out
a.out: need at least one argument

$ ./a.out -
a.out: need at least two arguments
```

Note that those `PWD`, `SHLVL`, and `_` variables are put there by the shell
that is run internally as part of `system(3)`.  That is OK.

# Option processing

(If we got there in the lecture)

- instead of `-` for `env`, use the `-i` option as is in the standard
