#!/usr/bin/env bash

for TEST in ./bin/*
do
    NAME=${TEST#"./bin/"}
    PRECISION=${NAME: -3}
    NAME=${NAME::-4}
    OUTPUT=`./${TEST} 12 1024 100000000 32`
    echo "${NAME},${PRECISION},${OUTPUT}"
    sleep 10
done
