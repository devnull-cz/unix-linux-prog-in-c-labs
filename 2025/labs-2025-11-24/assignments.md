
# Lock file with waiting

Change the
[`file-locking/file-locking.c`](https://github.com/devnull-cz/unix-linux-prog-in-c-src/blob/master/file-locking/fcntl-locking.c)
to busy wait when the lock is held.

Then change it again to avoid busy waiting, i.e. use pipe() as a waiting mechanism.

# Palindrome (redux)

- check if file contents is a palindrome using memory mapped file
  - verify that the RSS/size of the program is limited even for very
    large (think MiB/GiB) palindromatic files
  - set the exit code to 1 if the file is palindomatic or to 0 if not

# Questions

- is SIGCHLD always sent when child terminates ?
  - does it depend on `wait()`/`waitpid()`
- what happens on `wait()`/`waitpid()` after SIGCHLD is explicitly ignored ?

# use sigqueue to send data between processes

Fork a child process that will enter a loop in which it will send a set of numbers to the parent process
using `sigqueue()`. Use `SIGUSR1`.

Notes:
  - beware of signal races: if the parent installed the handler only after returning from `fork()`, the child might have sent its first `SIGUSR1`.
    This might make the parent exit if the signal was delivered before it completed `sigaction()` because the default action for this signal is to terminate the process. 
  - `SA_SIGINFO` flag has to be set, otherwise the siginfo structure will contain garbage in the `si_value` member
  - if waiting for the child with wait(), the `SA_RESTART` flag has to be used, otherwise signal delivery will cause the `wait()` to be interrupted
    - alternatively check the `errno` to be `EINTR`

# Signal chain

- write a program that will create a chain of N processes, each child creates
  the next one (hint: recursion):

```
  parent
    -> child_1
        -> child_2

             -> ...

                 -> child_N
```

- usage: `./a.out <number_of_children>`
- each process waits for the `SIGTERM` signal
- either use synchronous signal handling or install signal handler (has to be safe!)
- last child (`child_N`) sends the `SIGTERM` signal to its parent and then to itself
- once SIGTERM arrives, it will send it "upstream" and exit
  - thus the signal will travel all the way to the parent

## NOTES

  - use waitpid(2) or install `SIGCHLD` handler to get rid of the zombies
  - make sure the signal is set to the correct processes only
    - i.e. not the shell
    - use process group number to verify
    - introduce a kill() wrapper, use assert()
  - can the whole process group be killed with single signal if it does
    not have the SIGTERM handling ?

# Parent/child synchronization via signal

- write a program that creates a child process
  - The child will wait for the parent to signal (SIGUSR1) and only then starts
    running a loop (print/sleep) with finite iterations
  - the parent will wait for the child to send a signal (SIGUSR2) that it
    completed the loop
- construct the program as correcly as possible (i.e. avoid signal races)
  - hint: sigsuspend()
