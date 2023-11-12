#/bin/bash

output=$( $MYSH test-023.mysh 2>&1 >&- )

# We expect a syntax error in the last command.
(( $? == 0 )) && exit 1

# Every syntax error is expected to have the "syntax" string in it.
echo "$output" | grep -q "syntax"
