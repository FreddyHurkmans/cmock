#!/bin/bash

CMOCK='../src/cmock.py'

REF_H="_ref.h"
REF_C="_ref.c"
MOCK_H="_mock.h"
MOCK_C="_mock.c"
MOCK_H_OUT="_mock_out.h"
MOCK_C_OUT="_mock_out.c"
TEMPFILE="mock.out"

function GenerationTest {
    slash='/'
    path=$1$slash
    file=$path$2
    base=$path$3
    options=$4
    error=0

    $CMOCK $options $file
    if [ $? -ne 0 ]
    then
        >&2 echo -e "Mock generation failed for $file, used options: '$options'\n\n"
    else
        tail -n+11 $base$MOCK_H > $base$MOCK_H_OUT
        tail -n+11 $base$MOCK_C > $base$MOCK_C_OUT
        diff $base$REF_H $base$MOCK_H_OUT > $TEMPFILE
        if [ $? -ne 0 ]
        then
            echo "error in $base$MOCK_H_OUT:"
            cat $TEMPFILE
            error=1
        fi
        diff $base$REF_C $base$MOCK_C_OUT > $TEMPFILE
        if [ $? -ne 0 ]
        then
            echo "error in $base$MOCK_C_OUT:"
            cat $TEMPFILE
            error=1
        fi
        if [ $error -eq 0 ]
        then
            rm $TEMPFILE $base$MOCK_H $base$MOCK_C $base$MOCK_H_OUT $base$MOCK_C_OUT
        fi
    fi
}

# files in current directory
FILES=`find . -maxdepth 1 ! -name '*_*' -name '*.h'`
for file in $FILES
do
    if [[ $file != *"_"* ]]
    then
        path=$(dirname $file)
        file=$(basename $file)
        base=$(basename $file .h)
        cmockOptions=""
        if [ "$file" == "string2.h" ]
        then
            cmockOptions="-charstarIsInputString"
        fi
        GenerationTest $path $file $base $cmockOptions
    fi
done
