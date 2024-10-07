# Linker and libraries

## minimal linker options for trivial program

Write a trivial program (where e.g. `main()` calls `printf()` and exits) and run the compiler with the `-###` option
to see the linker options used to build the binary. Compile the program using the `-c` compiler option
and `ld`, using the options from the `-###` run. Try to reduce the set of linker options to minimum (so that the program still runs).

## runtime path vs. library search path

- write two dynamic libraries, `liba.so` and `libb.so`, and a program `prog` (compiled from `main.c`)
- `liba` will define a function `fna` which calls a function `fnb`
- function `fnb` will be defined in `libb`
- design `fna` and `fnb` as you wish just make sure they return something based
  on `argv[1]`, and print that argument out from `main` at the beginning
- `main()` from `main.c` only calls function `fna`
- make sure you can call the program from a local directory as `./prog`, and
  also from the `/` directory using a full path.

# Makefile
- write a makefile for the previous task
- use `touch(1)` to verify you only rebuild what is necessary and nothing else

# libmin, libmax and makefiles

Makefiles: let's assume GNU make for now

## Implement another program and a dynamic library

- start without makefiles
- the dynamic library will be called `libmin.so`
- it will implement one function:
```
int min(int a[], ssize_t len); // return minimum value
```
- the library source will comprise of the following two files:
  - `libmin.h`
  - `libmin.c` - will include libmin.h
- the program will be in `main.c`, compiled into `main` binary and will be
  dynamically linked against `libmin.so`
- `main.c` assumes valid numbers as its command line arguments
- create a numbered array in `main()` (see the prototype above), fill it with
  numbers from the arguments.  Remember, you need to convert the string
  arguments to numbers.
- call min() and print its result to stdout
- now, how do you tell:
  - `libmin.so` is a dynamic library
  - `libmin.so` defines the `min` function (rather than taking it from
    elsewhere)
  - `main` is linked against `libmin.so`

## Construct a Makefile for the above

- use usual targets: `all`, `clean`
- use automatic `gmake` variables (preceded with the '@' char)
- use wildcard rule for `*.c` => `*.o` files
- header files => C files dependencies
- use phony targets (clean) if using GNU make

## Implement a maximum function

`int max(int a[], ssize_t len); // return maximum value`

similarly to `libmin`, i.e. `libmax.[ch]`, `libmax.so`, ...

- and link main with both libraries
- 1st argument of your command will be now `min` or `max` string and based on
  that a given function will be chosen (and therefore the specific library will
  be used)

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
