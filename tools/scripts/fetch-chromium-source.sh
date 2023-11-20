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

if [ $# -ne 2 ]; then
  abort 1 "Usage: $0 <release-tag-commit-id> <chromium-version>"
fi

pushd "$(dirname "$0")"

commit="$1"
version="$2"

chromium_tarball="chromium-$version.tar.gz"

topdir="$PWD"
outputdir="$topdir/chromium-tarballs"

mkdir -p $outputdir

fini() {
  local retval="$?"

  [ -d $topdir/dep_tools ] && rm -rf $topdir/dep_tools

  exit "$retval"
}

trap fini EXIT

git clone -q --depth 1 https://chromium.googlesource.com/chromium/tools/depot_tools.git
[ $? -ne 0 ] && abort 1 "git clone depot_tools failed"

pushd depot_tools
commit_hash="$(git rev-parse --short HEAD)"

rm -rf ./.git*

export PATH=$PATH:$PWD

mkdir -p _tmp_ && pushd _tmp_

cat << EOF > .gclient
solutions = [
  {
    "name": "src",
    "url": "https://chromium.googlesource.com/chromium/src.git",
    "managed": False,
    "custom_deps": {},
    "custom_vars": {},
  },
]
EOF

set +x
gclient sync --revision src@$commit --no-history
[ $? -ne 0 ] && abort 1 "ERROR: gclient sync failed"
set -x

find ./src -name '.git' -type d | xargs rm -rf

tar -I 'gzip -9' -cpf $chromium_tarball src/
[ $? -ne 0 ] && abort 1 "ERROR: chromium tar creation error"

mv $chromium_tarball $outputdir/
[ $? -ne 0 ] && abort 1 "ERROR: mv chromium"

popd # _tmp_

rm -rf _tmp_

git clean -xxfd
popd # depot_tools

find depot_tools -name '.git' -type d | xargs rm -rf

depot_tools_tarball="depot_tools-$commit_hash.tar.xz"

tar -I 'xz -9' -cpf $depot_tools_tarball depot_tools
[ $? -ne 0 ] && abort 1 "ERROR: depot_tools tar creation error"

rm -rf depot_tools

mv $depot_tools_tarball $outputdir/
[ $? -ne 0 ] && abort 1 "ERROR: mv depot_tools"

popd # top
