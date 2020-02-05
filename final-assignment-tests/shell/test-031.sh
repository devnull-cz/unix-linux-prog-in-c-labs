#/bin/bash

# Catch bad handling of file descriptors. This number could be lower
# however catches most glaring mistakes.
ulimit -n 256

$MYSH test-031.mysh 2>&1
exit 0
