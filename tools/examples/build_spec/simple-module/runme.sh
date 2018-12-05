#! /bin/bash

WDIR=$(dirname $(readlink -m $0))
$WDIR/../../../scripts/build_spec.sh $WDIR/simple-module.spec
