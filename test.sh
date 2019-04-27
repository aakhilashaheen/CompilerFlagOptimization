#!/bin/bash -x

flag=$1

cd redis-latest
make distclean

export CC="gcc"
export OPT=""
unset REDIS_CFLAGS
unset REDIS_LDFLAGS
export CFLAGS="$flag"
export LDFLAGS="$flag"
make

echo "$flag"

cd src
./redis-server &

sleep 1

./redis-benchmark

#kill server process
pkill redis-server

