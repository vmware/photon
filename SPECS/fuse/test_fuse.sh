#!/bin/bash
mkdir example/test_fuse
example/hello -f example/test_fuse &
hello_pid=$!
example_file=example/test_fuse/hello
#check for fs to be up
for i in `seq 1 5`;
do
    if [ -f $example_file ]; then
        break
    fi
    sleep 1
done
expected="Hello World!"
actual=$(cat example/test_fuse/hello)
if [ "$actual" != "$expected" ];
then
    echo $actual doesnot match with $expected
    exit 1
fi
kill $hello_pid
