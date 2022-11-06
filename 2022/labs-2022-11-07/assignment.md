# Creating processes

## closing file descriptors across exec

Produce 2 programs:
  1. Create and open set of files given by `argv`, mark these file descriptors to be close-on-exec, 
     create new process via `exec` syscall and pass the fd numbers as arguments to the new program
  3. programatically verify that file descriptors given by `argv` are closed

I.e. the first program will execute the second program.

