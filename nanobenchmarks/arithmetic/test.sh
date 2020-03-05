#!/usr/bin/env bash

for TEST in ./bin/*
do
    ITERATIONS=100000000
    NAME=${TEST#"./bin/"}
    PRECISION=${NAME: -3}
    NAME=${NAME::-4}
    if [[ $NAME == *"div"* ]]
    then
        ITERATIONS=1000
    fi
    if [[ $NAME == *"rcp.rn"* ]]
    then
        ITERATIONS=10000
    fi
    if [[ $NAME == *"rem"* ]]
    then
        if [[ $PRECISION == *"32"* ]]
        then
            ITERATIONS=1000
        else
            ITERATIONS=100
        fi
    fi
    if [[ $NAME == "rsqrt.approx" ]]
    then
        if [[ $PRECISION == "f64" ]]
        then
            ITERATIONS=10000
        fi
    fi
    OUTPUT=`./${TEST} 12 1024 ${ITERATIONS} 32`
    echo "${NAME},${PRECISION},${OUTPUT}"
    sleep 10
done
