#/bin/bash

# wc(1) produces leading spaces on macOS
$MYSH -c 'echo X; echo AA; date | cat | cat | sort | wc -l; echo ZZZ' | \
    sed -e 's/^ *1/1/g'
