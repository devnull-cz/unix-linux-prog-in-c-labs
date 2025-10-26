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

Think first, then verify your hypothesis with `pstree -p -s -t <pid>` or by using the `f` output modifier (*process forest*) of `ps`.

Note: this is assuming a system with the `pstree` command (e.g. Linux distribution or FreeBSD).

## Fork bomb

Read https://en.wikipedia.org/wiki/Fork_bomb and implement fork bomb in C.
Run and observe the results.

**Note: be warned that it might deplete system resources on the system the program is run on**

## exec `vi -R /etc/passwd`

Do not use `fork()`. Start with `execl()`, then try `execv()`. Then try `posix_spawn()`.

## supply environment variable

Execute `sudo vipw` with the `EDITOR` environment variable set to your favorite editor.
You will have to use the `--preserve-env` option for sudo, because it sanitizes the environment by default.

If you cannot execute `sudo` on your system, use the `env` program instead of the `sudo vipw` to see that the
variable setting is in effect.

## different process tree

Create the following process tree:

```

   parent_1
   fork()  --> child_1 (parent_2)
               fork() -------------> child_2

```

Each process:
  - prints its PID, parent PID, process group ID
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

The main process should wait for all the children to complete.

Verify all output went to the file "`output`". Also make sure any errors printed to `stderr`
by `wc` are printed to the console (e.g. when `wc` does not have sufficient permissions to read the file).

Lastly, think about what is going on in terms of file descriptors used by the child programs,
the global file table and the file offset.

# File I/O

## `readdir`

- write a program that will generate output similar to `ls -R`
	- choose your own output form but increase indenting for each level of
	  directories

## `rm -r`

- implement `rm -r <dir>`
  - be careful...
  - I suggest to first print what would be done before the next version actually does it
  - create a short program to generate a random directory structure
  
## `getent`

- traverse the password database using the `(set|get|end)pwent` and print all
  usernames, and possibly some more information from the `passwd` structure.
