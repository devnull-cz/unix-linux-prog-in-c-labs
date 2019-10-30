
# Generic notes

- check all return values and react accordingly (err(3) family of functions)
  - okay, maybe except those from printf() family of functions and close(2)
- write unit tests
  - ideally driven by Makefile
  - ideally run them in CI environment (like Travis, Github actions etc.)

# Tasks

## palindrome file detection
  - definition: a word that reads the same way forwards or backwards, e.g. 'noon', 'ada', etc.
    https://en.wikipedia.org/wiki/Palindrome
    - palindromatic file is a that whose contents form a palindrome
  - optional: the detection should be case insensitive
    - add getopt() option to control this behavior
  - usage: `./a.out <file>`
    - returns 0 if the contents of the file form a palindrome, 1 otherwise
      - side note: what should /bin/false or /usr/bin/false return and what is the reality ? (on different Unix systems)
                   and what does POSIX say ? (go and look into the standard)
  - implementation: there are multiple choices (using index walkers, recursive,
    read all of it in and compare reversed string, ...)
    - use read()+lseek() to retrieve single character on given position
    - usig stat(2)/fstat(2)/lstat(2) is not allowed

## directory traversal with stat
   - usage: ./a.out directory
   - will traverse the directory recursively and compute the average length in bytes of all regular files found
   - bonus points: follow symlinks
     - extra bonus points: do not follow symlinks outside of the top level directory
   - bonus points: print files that are bigger than the average found (requires 2nd traversal)
     - think about beautiful implementation: use callbacks (function pointer)
       with context parameter to be able to switch the action (1st traversal
       uses function to compute the average, 2nd traversal uses function to
       print certain entries)
   - use macros (to detect special directory entries)
   - avoid using global variables in any of the variants
   - how to allocate enough memory for path on given file system ?
     - see pathconf(2)

## utmp modification (standard hacker tool from the 90's)

What the h\* is utmp ? See https://en.wikipedia.org/wiki/Utmp

   - write a program that removes entries matching specification from utmp database
     - entry specification: username + tty, the tty can be optional
   - sufficient to read/process one entry at a time
   - use who(1) to verify (write a simple test, remember Github + Travis ?)
   - do not update the file in place, rather create new one by removing the entries and move it to the original location
     - make sure to preserve ownership/permissions/times - use stat(2)
   - there are 2 formats of utmp entries: historical (utmp) and extended/standard (utmpx)
     - see what the system you will be writing this on uses and stick with that (i.e. either use utmp.h or utmpx.h) 
- e.g. macOS uses utmpx (/var/run/utmpx)
