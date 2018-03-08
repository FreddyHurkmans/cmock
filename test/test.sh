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
    error=0

    $CMOCK $file
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
        GenerationTest $path $file $base
    fi
done
