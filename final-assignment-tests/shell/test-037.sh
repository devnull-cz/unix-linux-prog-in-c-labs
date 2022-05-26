#/bin/bash

dir=long-path-123456
count=128

function test_input {
    seq $count | while read i; do
        echo -e "mkdir $dir; cd $dir"
    done
    echo "pwd"
}

n=$( test_input | $MYSH | tr '/' '\n' | grep "^${dir}$" | wc -l )
rm -rf $dir

(( $n != $count )) && echo "Count expected $count, was $n" && exit 1
exit 0
