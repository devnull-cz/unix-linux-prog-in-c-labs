# `readdir`

- write a program that will generate output similar to `ls -R`
	- choose your own output form but increase indenting for each level of
	  directories

# `rm -r`

- implement `rm -r <dir>`
	- be careful...
	- I suggest to first print what would be done before the next version
	  actually does it
	- create a short shell script to generate a random directory structure
		- you can get a small random number like this, for example (bash
		  specific): `echo $(($RANDOM % 8))`

# `getent`

- traverse the password database using the `(set|get|end)pwent` and print all
  usernames, and possibly some more information from the `passwd` structure.
