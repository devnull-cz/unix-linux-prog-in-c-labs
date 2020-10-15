
# libmin, libmax and makefiles

Makefiles: let's assume GNU make for now

## implement a program and dynamic library

- start without makefiles
- the dynamic library will be called `libmin.so`
- it will implement one function: `int min(int a[], ssize_t len); // return minimum value`
- the library source will be comprised of 2 files:
  - `libmin.h`
  - `libmin.c` - will include libmin.h

- the program will be in `main.c`, compiled into `main` binary and will be linked against `libmin.so`
- `main.c` will create array of the size of program arguments, fill it with the numbers, call min() and print the result to stdout
- use file(1), nm, ldd, readelf to inspect `libmin.o, libmin.so, main.o, main`
- run the program with various LD_DEBUG values to see dynamic linker
 processing (e.g. 'libs', 'symbols')

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
- 1st argument will be now "min" or "max" and based on that
 given function (and therefore library will be used)

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

bonus: use Makefile includes to minimize sharing/copying
              (hint: use top-level makefile and include it in subdirs)

## [optional] build with various compilers in CI environment
     
- use Travis / Github Actions

## [optional] write simple test script

- run it in the CI environment above


# ASCII histogram

  - command line arguments are positive integers
    - exit on non-number argument
    - if less arguments than default number of columns (75), use some heuristics
      for the number of columns (e.g. `argc / 2`)
  - draw a histogram of the input integers
  - optional: log scale (see math.h and log(3))

```
$ for i in `seq 100`; do args="$args $RANDOM"; done
$ ./a.out $args
#                                           #                        #  #
#                                     #     #             #          #  #
#           #          #              #     #             # #        #  #
#           # ##    #  #      #       #     #  #   #      # #        #  #
#         # # ##  # #  # #    #  # # ##    ### #  ##      # #        #  #
#      #  ######  # ## # #   ##  # # ##    ### #  ##   #  # # #      #  # #
# # #  ## ####### # ## # #   ## ## ####  # ###### ##   #  # # #      # ## #
# # #  ## ####### # #### # # ## ## ##### # ########## ### # # #    # #### #
# # # ########### # ############## ##### ############ ### # # # ###########
# ### ########### # ############## ##### ############ ### # ### ###########
# ### ########### # #################### ############ ######### ###########
##### ############# ########################################### ###########
##### ############# #######################################################
###########################################################################
```
