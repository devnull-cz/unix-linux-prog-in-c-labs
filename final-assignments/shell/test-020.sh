#/bin/bash

# This must take 3 seconds even that the "date" commands exit right away.  The
# latter regexp is for macOS.
#
# Use -p for portable output.
/usr/bin/time -p $MYSH -c 'date | sleep 3 | date' 2>&1 | \
    egrep 'real.*3.0|3\... real'
