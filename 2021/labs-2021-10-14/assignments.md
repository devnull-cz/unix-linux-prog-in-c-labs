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


# Environment

- write a simple `env(1)`-like program
  - `env [-] [varname=value [varname=value ...]] [command]`
  - if the first argument is `-`, clear the environment before executing the command
  - set environment variables in the caller if present on the command line
  - to execute the command, use `system(3)`
  - if the command is not given, print all environment variables along with their values to stdout
  - the command is just one argument (program name)
  - all other arguments aside from the last one are variable definitions
  - do reasonable error checking

Example:

```
$ ./a.out env
<long output of environment variables>

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

## Optional tasks

Extra tasks:
  - accept arguments to the command
    - i.e. `env [-] [varname=value [varname=value ...]] [utility [argument ...]]`
  - instead of `-` for `env`, use the `-i` option as is in the standard
  - implement `-u`


# getopt

- check out http://github.com/devnull-cz/unix-linux-prog-in-c-src/blob/master/getopt/getopts.sh, then write the same
  functionality in C.

```
$ ./getopts.sh
usage: getopts.sh command [-c code] [filename [filename [...]]]

$ ./getopts.sh boot -c 11 xxx yyy
first param (command): boot
option -c set to '11'
...done reading option arguments
filenames: xxx yyy

$ ./getopts.sh boot -x 11 xxx yyy
first param (command): boot
./getopts.sh: illegal option -- x
usage: getopts.sh command [-c code] [filename [filename [...]]]

$ ./getopts.sh attach
first param (command): attach
...done reading option arguments
no filenames entered
```

It is recomended to write some unit tests. Look at `getopt-tests.c`.
