
# Palindrome (redux)

- check if file contents is a palindrome using memory mapped file
  - verify that the RSS/size of the program is limited even for very
    large (think MiB/GiB) palindromatic files
  - set the exit code to 1 if the file is palindomatic or to 0 if not

# Questions

- is SIGCHLD always sent when child terminates ?
  - does it depend on `wait()`/`waitpid()`
- what happens on `wait()`/`waitpid()` after SIGCHLD is explicitly ignored ?

- how to handle SIGPIPE ?
  - hint: https://www.pixelbeat.org/programming/sigpipe_handling.html

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

  - use waitpid(2)
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
