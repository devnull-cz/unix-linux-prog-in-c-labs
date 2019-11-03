#/bin/bash

$MYSH -c 'echo A; echo B; ./nonexistent-xxx; exit;' 2>/dev/null
(( $? == 127 )) && exit 0
exit 1
