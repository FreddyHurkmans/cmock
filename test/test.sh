#!/bin/bash

CMOCK='../cmock.py'
FILES=`find . ! -name '*_*' -name '*.h'`

REF_H="_ref.h"
REF_C="_ref.c"
MOCK_H="_mock.h"
MOCK_C="_mock.c"
MOCK_H_OUT="_mock_out.h"
MOCK_C_OUT="_mock_out.c"
TEMPFILE="mock.out"

for file in $FILES
do
  if [[ $file != *"_"* ]]
  then
    error=0
    file=$(basename $file)
    base=$(basename $file .h)
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
  fi
done


#rm *_mock.[ch]