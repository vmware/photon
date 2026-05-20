#!/bin/bash

_LOC=$(dirname $(readlink -f "$0"))
for patch in $(ls "${_LOC}"); do
  [[ $patch =~ .*.sh ]] && continue
  pushd /
  patch -p1 -f < "${_LOC}/${patch}"
  popd
done
