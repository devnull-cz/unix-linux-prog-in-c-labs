#/bin/bash

count=1000
u=$( uname )
n=$( seq $count | while read i; do
	echo "uname | cat | cat | cat | sort | uniq"
done | $MYSH | grep "^${u}$" | wc -l )

(( $n != $count )) && echo "Count expected $count, was $n" && exit 1
exit 0
