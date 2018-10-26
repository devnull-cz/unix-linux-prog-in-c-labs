# Tasks

1) palindrome file detection
  - a word that reads the same way forwards or backwards, e.g. 'noon', 'ada', etc.
    https://en.wikipedia.org/wiki/Palindrome
  - usage: ./a.out <file>
    - returns 0 if the contents of the file form a palindrome, >0 otherwise
      - side note: what should /bin/false or /usr/bin/false return and what is the reality ? (on different Unix systems)
                   and what does POSIX say ? (go and look into the standard)
  - use read()+lseek()

2) reverse bytes in a file
  - usage: ./a.out infile outfile
  - variant A (naive)
    - byte by byte (similar to the previous task)
  - variant B (better)
    - use buffer - add '[-b bufsiz]' to the usage
      - start with 1k, compare the performance to previous variant
        - Q: how to measure this properly ? (e.g. for each run create new file filled with random values)
      - experiment with various buffer sizes - which one performs the best ?
  - variant C (for next time)
    - use mmap()

3) directory traversal with stat
   - usage: ./a.out directory
   - will traverse the directory recursively and computes the average length in bytes of all regular files found
   - bonus points: follow symlinks
     - extra bonus points: do not follow symlinks outside of the top level directory
   - bonus points: print files that are bigger than the average found (requires 2nd traversal)
   - avoid using global variables in any of the variants

4) utmp modification (standard hacker tool from the 90's)
   https://en.wikipedia.org/wiki/Utmp
   - write a program that removes entries matching specification from utmp database
     - entry specification: username + tty, the tty can be optional
   - sufficient to read/process one entry at a time
   - use who(1) to verify (write a simple test, remember Github + Travis ?)
   - do not update the file in place, rather create new one by removing the entries and move it to the original location
     - make sure to preserve ownership/permissions/times - use stat(2)
   - there are 2 formats of utmp entries: historical (utmp) and extended/standard (utmpx)
     - see what the system you will be writing this on uses and stick with that (i.e. either use utmp.h or utmpx.h) 
- e.g. macOS uses utmpx (/var/run/utmpx)

# Testing notes

dead-simple solution to unit testing:

```
PROG=./a.out                                                                    
                                                                                
FILES=noona.txt noon.txt noona.txt                                              
test:                                                                           
        @for file in $(FILES); do \                                             
                $(PROG) $$file >/dev/null; \                                    
                if [ $$? -ne 0 ]; then echo "FAILED: $$file"; ret=1; else \     
                echo "PASSED $$file"; fi \                                      
        done; exit $$ret                                                        
                                                                                
test2:                                                                          
        ./check.sh $(PROG) $(FILES)
```

Of course, there should be a set of negative tests (that make sure the program fails on input which are not palindomatic files). The second target (`test2`) is possibly more flexible as one does not have to battle with shell vs. Makefile intricacies. What is inside `check.sh` ? Well, pretty much the same as is in the Makefile:

```shell
#!/bin/bash

PROG=$1
shift
ret=0

for file in $*; do
	$PROG $file >/dev/null
	if [[ $? -ne 0 ]]; then
		echo "FAILED: $file"
		ret=1
	else
		echo "PASSED $file"
	fi
done

exit $ret
```
