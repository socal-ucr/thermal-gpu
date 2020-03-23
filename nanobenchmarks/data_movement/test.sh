#!/usr/bin/env bash
for TEST in ./bin/*
do
    ITERATIONS=100000000
    NAME=${TEST#"./bin/"}
    PRECISION=${NAME: -3}
    NAME=${NAME::-4}
    if [[ $NAME == *"st"* ]]
    then
        ITERATIONS=2000
    fi
    if [[ $NAME == *"prefetch"* ]]
    then
        ITERATIONS=2000
    fi

    OUTPUT=`./${TEST} 12 1024 ${ITERATIONS} 32`
    echo "${NAME},${PRECISION},${OUTPUT}"
#    sleep 10
done
