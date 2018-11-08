# Tasks

- warmup:
  - Fork a process, sleep in the child for specified timeout using sleep(3). 
  - In the parent, wait for the child, exit.
  - see what happens if parent does not wait on the child to finish
```
  usage: ./a.out <timeout_in_seconds>
```

- Parent forks a child and waits for it.  Child sleeps for ever. 
  - Kill the child from the shell.  Parent will print the signal number.

Example:
```
$ ./a.out &
[1] 34926
CHILD: my pid is 34927.
$ kill -9 34927
PARENT: child killed by signal 9.
```
- reimplement daemon(3)
  - basic idea: fork a new child, exit the parent
  - make it robust w.r.t. setsid(2) failure
  - make sure to behave correctly w.r.t. file descriptors (verify with lsof(1))
  - write tests

- fork a child, fork again in the child, and again until specified count of children is met.
  - Every parent waits for its child.
  - Exec pstree(1) with -psa options in the last child on itself (i.e. `pstree -psa <childs-pid>`). 
  - Exit then.
```
  usage: ./a.out <num_children>
```
  - on Solaris use `ptree <pid>`, on macOS install `pstree` from Homebrew
  - the goal is to create a cascade of processes, not flat tree ("broom")
  
- parent creates a child that will allocate specified number of memory on the heap, 
  fill it with given byte and exit.
  - Parent will then report high-water memory usage using wait4().
  - see getrusage(2) man page for details about the rusage structure members
  - try the same via GNU time (e.g. `/usr/bin/time -v -- /some/program`) and see 
    if the reported values match
  - see https://github.com/gsauthof/cgmemtime for more sophisticated solution
  
- Process a file from argv[1] to build argv for execv(2).  You must not
  use a statically allocated `*argv` array for pointers as the number of
  arguments may be unlimited.  There is one argument per line in the file.
  You may only process the file once, i.e. you must not first read the
  file into memory, then count the lines, allocate argv, then process the
  file again to populate the argv.  You may not use mmap(2) even if you
  know how to.
  - Hint: use macros from <queue.h> to build a linked list of arguments
  while reading the file, then allocate and populate argv using the linked
  list.

  - Example #1:
```
$ cat args
/bin/echo
hello
world

$ ./a.out args
hello world
```
  - Example #2:
```  
  $ cat args
  /usr/bin/touch
  foo
  bar
  ahem ahem
  
  $ ./a.out
  $ ls -1
  foo
  bar
  ahem ahem
```

# Debugging

Use `strace` with the follow option (-f) to trace across forks. Optionally, store the output into a file (use -o) so that the tracing output is not mixed with program output. Also, see what filtering capabilities are there (-e) to trace just a subset of system calls.

Try to run the programs under debugger to see what happens on fork.

# Notes

- avoid using system(3) at all costs. Besides unnecessarily spawning shell, it might introduce security vulnerability. See https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152177
