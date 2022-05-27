#/bin/bash

dir=long-path-123456
tmpdir=$(mktemp -d)

# PATH_MAX can be as low as 256, so were safe ${#dir} * 8 = 128
count=8

function test_input {
    seq $count | while read i; do
        echo -e "mkdir $dir; cd $dir"
    done
    echo "pwd"
}

n=$( cd $tmpdir; test_input | $MYSH | tr "/" "\n" | grep -c "^${dir}$" )
rm -rf $tmpdir

(( $n != $count )) && echo "Count expected $count, was $n" && exit 1
exit 0
