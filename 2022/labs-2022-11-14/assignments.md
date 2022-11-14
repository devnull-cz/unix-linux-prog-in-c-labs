
# Construct a shared library

Produce a shared library (`libmy.so.`) and a program liniking with it. Call a function from the shared library in the program.

Write Makefile(s).

# Plugin framework

Produce program that will search for all `*.so` files inside current directory and will load them
using the dynamic linker APIs. Call `void foo(char *)` for all the libraries found.

The `foo()` function might e.g. pass the argument to `printf()`. Implement at least 2 different
shared libraries that implement this plugin framework API.

Gracefully skip the libraries that do not adhere to the plugin framework APIs.
Copy one of the system libraries (from e.g. `/usr/lib` directory) to the current directory to test this out.

# Zombie army

Create a program that produces selected number of zombies and then exits.
Observe the zombies being handled by the init(8) process.

Check the state of the zombie processes with ps(1).

Note: on some systems, the child reaping functionality of init was subsumed into
service management daemons such as `systemd`.

usage: `./a.out <zombie_num>`

## sub-task

Fix the zombie problem.


## `pipe`

- Check out slide "Example: a pipe between two processes" and implement:

```
ls / | wc -l
```
- Do not use any existing code, just use the slides.

## `pipe` with not closing some descriptors

- In the notes below slide "Example: a pipe between two processes", we mentioned
  what may happen if we do not close two file descriptors (one in the consumer,
  the other one in the producer).

- one by one, do no close it and figure out how to verify that it may lead to
  the situation described.

## `wait`

- from the unix-linux-prog-in-c-src repo, take the first block comment and
  re-implement it.  **Do not look at the code.**  Use slides only.  Making
  mistakes and figuring it out is the best way to learn the stuff.

```
unix-linux-prog-in-c-src/wait$ head -34 wait.c
/*
 * An example program to see how waitpid(3) works.  Start the program.  After
 * that, you can do 4 different things:
 *
 *   (1) wait quietly for 30 seconds to see the parent report sleep's return
 *       value which should be 0
 *   (2) kill sleep (use the child's PID printed upon startup) to see the
 *       signal number used.  Try different signals (kill <PID>, kill -9 <PID>,
 *       ...)
 *   (3) stop the child to see that the parent gets notified about that. You
 *       can stop a process by sending it a stop signal: kill -STOP <PID>.
 *       Again, use the child's PID.
 *   (4) continue the child by "kill -CONT <PID>"
 *
 * The parent will continue to report on the child states until the child is
 * finished.  Note that if the sleep is stopped it will not get the 30 seconds
 * timeout unless it gets continued again.
 *
 * Note that when the child is killed by a signal, the status word itself
 * may contain just the signal number.  However, that is just a coincidence and
 * can be implementation dependent!  Always use the WIFSIGNALED and WTERMSIG
 * macros to get the signal number.
 *
 * If WUNTRACED was not used in the flags parameter, the parent would not be
 * notified about stopped children.  Try to remove it and then "kill -STOP"
 * the child to see that.  The same stands for continuing the child - the parent
 * would not get notified about continued children unless WCONTINUED is present.
 * Also note that stopping an already stopped process is not reported, the same
 * stands for continued processes.
 *
 * See waitpid(3) for more information.
 *
 * (c) jp@devnull.cz
 */
```

## double `pipe`

- Implement:

```
$ cal | head -1 | tr '[[:lower:]]' '[[:upper:]]'
   NOVEMBER 2020
```

- This task is good for understanding that by common code you actually need to
  manage three different processes.

- If it prints what you expect but hangs after that, you forgot to close all the
  needed descriptors you were supposed to close.
