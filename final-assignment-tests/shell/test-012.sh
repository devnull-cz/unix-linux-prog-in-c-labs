#/bin/bash

# wc(1) produces leading spaces on macOS
$MYSH test-012.mysh | sed -e 's/^ *1/1/g'
