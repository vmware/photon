#!/bin/bash

#set -x

echoerr() {
  echo -ne "\n$*\n" 1>&2
}

abort() {
  local rc=$1
  shift
  echoerr "$*"
  exit $rc
}

if [ $# -ne 1 ]; then
  abort 1 "Usage: $0 <dictionaries-version>"
fi

version="$1"
work_dir="$(mktemp -d)"

declare -A supported_langs=(
  ["en"]="en_US"
  ["en-GB"]="en_GB"
)

files_needed=(aff dic)
clone_url="https://github.com/wooorm/dictionaries.git"
clone_dir="dictionaries.git"
output_dir="$work_dir/dictionaries"
dictionaries_tarball="dictionaries-$version.tar.gz"

fini() {
  local retval="$?"

  if [ $retval -ne 0 ]; then
    rm -rf $work_dir
    echo "ERROR: Operation failed ..." 1>&2
  else
    echo "Tarball is available at $work_dir"
    rm -rf $clone_dir $output_dir
  fi

  exit $retval
}

trap fini EXIT

cd $work_dir

echo "Cloning repo ..."
if ! git clone -q --no-tags --depth 1 $clone_url $clone_dir; then
  abort 1 "ERROR: git clone $clone_url failed"
fi

mkdir -p $output_dir

echo "Packaging files ..."
cd $clone_dir
for k in ${!supported_langs[@]}; do
  lang_dir="dictionaries/$k"
  for fn in ${files_needed[@]}; do
    if ! mv $lang_dir/index.$fn $output_dir/${supported_langs[${k}]}.$fn; then
      abort 1 "ERROR: $k $fn file does not exist"
    fi
  done
done

cd $work_dir

echo "Creating tarball ..."
if ! tar -I 'gzip -9' -cpf $dictionaries_tarball $(basename $output_dir); then
  abort 1 "ERROR: $dictionaries_tarball creation error"
fi

echo "Done ..."
