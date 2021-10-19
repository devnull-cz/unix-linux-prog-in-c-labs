# Linker and libraries

- write two libraries, `liba` and `libb`, and a program `main.c`
- `liba` will define a function `fna` which calls a function `fnb`
- function `fnb` will be defined in `libb`
- design `fna` and `fnb` as you wish just make sure they return something based
  on `argv[1]`, and print that out from `main`
- `main()` from `main.c` only calls function `fna`
- make sure you can call the program from a local directory as `./a.out`, and
  also from the `/` directory using a full path.

# Makefile
- write a makefile for the previous task
- use `touch(1)` to verify you only rebuild what is necessary and nothing else

# libmin, libmax and makefiles

Makefiles: let's assume GNU make for now

## implement a program and dynamic library

- start without makefiles
- the dynamic library will be called `libmin.so`
- it will implement one function: `int min(int a[], ssize_t len); // return minimum value`
- the library source will be comprised of 2 files:
  - `libmin.h`
  - `libmin.c` - will include libmin.h

- the program will be in `main.c`, compiled into `main` binary and will be
  linked against `libmin.so`
- `main.c` will create array of the size of program arguments, fill it with the
  numbers, call min() and print the result to stdout
- how do you tell:
  - `libmin.so` is dynamic library
  - `libmin.so` defines the `min` function (rather than taking it from
    elsewhere)
  - `main` is linked against `libmin.so`

## construct set of Makefiles

- basic targets: `all`, `clean`
- use automatic gmake variables (preceded with the '@' char)
- use wildcard rule for `*.c` => `*.o` files
- header files => C files dependencies
- use phony targets (clean) if using GNU make

## implement maximum function

`int max(int a[], ssize_t len); // return maximum value`

similarly to `libmin`, i.e. `libmax.[ch]`, `libmax.so`, ...

- and link main with both libraries
- 1st argument of your command will be now "min" or "max" and based on that
 given function will be chosen (and therefore library will be used)

- use hierarchical build:
```
Makefile
main.c
libmin/
 Makefile
 libmin.c
libmax/
 Makefile
 libmax.c
```
  - divide and conquer: in order to build stuff in `libmin` from within the top
    level `Makefile`, run e.g. `cd libmin; make` as the command to refresh the
    (empty) target.  Do not put dependencies from subdirectories into the top
    level `Makefile`.
