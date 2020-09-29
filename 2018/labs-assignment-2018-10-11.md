- mysh: go through detailed task description
  - can start coding right away (parsing), do not have to wait until fork()/pipe()/exec() are explained
  - the shell cannot (and should not) be coded in couple of days
    - write your own unit tests
    
- demonstrate how to use Github+Travis
  - `.travis.yml` contents:
```yml
  language: c
  compiler:
  - clang
  - gcc
  script: make
```  
- more on C style (or coding style in general)
  - header include ordering, general ordering (license, includes, typedefs, defines, func prototypes, func definitions)

- tasks:
  - pre-warmup:
    - write a program that will define a void pointer to self
    - verify that this is the case via debugger (or debug prints)
    
  - warmup:
    - write a program that will print (to stdout) only penultimate line of input received on stdin
    - use getline(3)
    - be conservative in memory usage, use malloc()/free() to allocate the memory
    - exit with error in case of invalid input (at least 2 lines are required)
    
  - Program will get a list of arguments that are environment variable names.
    - The program will recognize 2 options:
        -a      will check that all variables are defined. If yes return 0,
                otherwise return 1.
        -o      will check that at least one variable is defined.
                If yes return 0, otherwise return 1.         

        Examples:
```
        $ ./main -a SHELL HOME
        0
        $ ./main -o SHELL NONEXISTENT
        0
        # (should print usage)
        $ ./main SHELL HOME PWD
```
    
  - environment variable manipulation
    - write a program that will create a set of new environment variables based on a static string of the form "XXXX=Y"
      where it will create env vars "XXXX", "XXX", "XX", "X" - all with the value of "Y"
      - use pointer arithmetics and putenv() for that, i.e. no memory will be allocated
      - print environment (see environ(7)) before and after the manipulation (with a separator)
      - what is the relationship between envp and environ ?
  
  - construct a library
    - it will implement function
      int min(int a[], ssize_t len);
    - and a program that will link against the library and call the min() function with sample inputs
    - write separate Makefiles for the program and the shared library
    - make sure runtime path is set correctly
