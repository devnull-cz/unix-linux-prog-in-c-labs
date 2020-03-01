#/bin/bash

# Note that bash prints warnings for environment variables not set.  However, we
# do not check the actual messages (there is no test-036.output), we only care
# about the exit value.  As 'pwd' was the last command, and it succeeded, we
# expect 0.  For example:
#
#	host-machine$ env - /bin/bash
#	bash: cd: HOME not set
#	$ cd -
#	bash: cd: OLDPWD not set
#	$ cd
#	bash: cd: HOME not set
#	$ pwd
#	/tmp
#	$ exit
#	host-machine$ echo $?
#	0
#
env - $MYSH test-036.mysh
