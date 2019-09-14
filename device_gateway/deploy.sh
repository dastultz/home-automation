#!/bin/bash

function copy_file() {
    echo "Copying $1 to /$1"
    ampy put $1 /$1
}

LD=".last_deploy"
if [ ! -f "$LD" ] ; then
    touch -t 201801010000 $LD
fi

FILES=`find . -name '*.py' -newer $LD  | grep -v ^./_ | cut -c3-`

for F in $FILES ; do
    copy_file $F
done

touch $LD

screen $AMPY_PORT $AMPY_BAUD