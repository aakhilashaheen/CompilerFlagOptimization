#!/bin/bash -x

flag="$1"
EXT1=$RANDOM
EXT2=$RANDOM
EXT3=$RANDOM

if [[ -e redis/ ]]; then
        pushd redis/
        git checkout 5.0.4
        popd
else
        git clone https://github.com/antirez/redis
        pushd redis/
        git checkout 5.0.4
        popd
fi

cd redis/src

make distclean

export CC="gcc"
export OPTIMIZATION=""
unset REDIS_CFLAGS
unset REDIS_LDFLAGS
export REDIS_CFLAGS="$flag"
export REDIS_LDFLAGS="$flag"
make

./redis-server &

./redis-benchmark -n 100000 -t set -r $EXT1 -q --csv >| ../../test.csv
./redis-benchmark -n 100000 -t set -r $EXT2 -q --csv >> ../../test.csv
./redis-benchmark -n 100000 -t set -r $EXT3 -q --csv >> ../../test.csv

#kill server process
pkill redis-server

make distclean
exit(0)
