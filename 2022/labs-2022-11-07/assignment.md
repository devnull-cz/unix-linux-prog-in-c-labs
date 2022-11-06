# Creating processes

## calling fork() repeatedly

Consider the following code:
```C
int
main(void)
{
  fork();
  fork();
  fork();
  sleep(42);
}
```

Questions:
  - how many processes will be running ?
  - how exactly will the process hierarchy look like ?

Think first, then verify your hypothesis with `pstree -p -s -t <pid>`.

## exec `vim /etc/passwd`

Do not use `fork()`.

## different process tree

Create the following process tree:

```

   parent_1
   fork()  --> child_1 (parent_2)
               fork() -------------> child_3
                                     fork()

```

Each process:
  - prints its PID and parent PID
  - will call `sleep(1)` before exiting.

### variant

The last process will exec `pstree -p -s -a` on itself. To convert PID to string, you can use
either `snprintf()` or `asprintf()`.

## closing file descriptors across exec

Produce 2 programs:
  1. Create and open set of files given by `argv`, mark these file descriptors to be close-on-exec, 
     create new process via `exec` syscall and pass the fd numbers as arguments to the new program
  3. programatically verify that file descriptors given by `argv` are closed

I.e. the first program will execute the second program.

## Count lines for files in a directory

Open file "`output`" for writing and redirect standard output to it. Then go through directory tree
starting at `argv[1]` and for each regular file do `fork()` and `exec()` of `wc -l` on that file.

Verify all output went to file file "`output`". Also make sure any errors printed to `stderr`
by `wc` are printed to the console (e.g. when `wc` does not have sufficient permissions to read the file).
