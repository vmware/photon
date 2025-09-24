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

pushd /tmp

commit="$1"
version="$2"

chromium_tarball="chromium-$version.tar.xz"

topdir="$PWD"
outputdir="$topdir/chromium-tarballs"

mkdir -p $outputdir

fini() {
  local retval="$?"

  [ -d $topdir/depot_tools ] && rm -rf $topdir/depot_tools

  exit "$retval"
}

trap fini EXIT

git clone -q --depth 1 https://chromium.googlesource.com/chromium/tools/depot_tools.git
[ $? -ne 0 ] && abort 1 "git clone depot_tools failed"

depotToolsOutDir="depot_tools.new"
pushd depot_tools
commit_hash="$(git rev-parse --short HEAD)"

mkdir -p ${depotToolsOutDir}/python-bin

files=(subprocess2.py gn gclient_utils.py LICENSE gn_helper.py)
files+=(gn.py gclient_paths.py)

cp -a ${files[@]} ${depotToolsOutDir}/

cp -a python-bin/python3 ${depotToolsOutDir}/python-bin
mv ${depotToolsOutDir} ..
popd

mv depot_tools depot_tools.bak
mv ${depotToolsOutDir} depot_tools

depot_tools_tarball="depot_tools-$commit_hash.tar.xz"

tar -I 'xz -9' -cpf $depot_tools_tarball depot_tools
[ $? -ne 0 ] && abort 1 "ERROR: depot_tools tar creation error"

mv $depot_tools_tarball $outputdir/
[ $? -ne 0 ] && abort 1 "ERROR: mv depot_tools"

rm -rf depot_tools
mv depot_tools.bak depot_tools
export PATH=$PATH:$PWD/depot_tools

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
gclient sync --revision src@$commit --no-history --shallow
[ $? -ne 0 ] && abort 1 "ERROR: gclient sync failed"
set -x

find ./src -name '.git' -type d | xargs rm -rf

: '
tar -I 'xz -9' -cpf $chromium_tarball src/
[ $? -ne 0 ] && abort 1 "ERROR: chromium tar creation error"

mv $chromium_tarball $outputdir/
[ $? -ne 0 ] && abort 1 "ERROR: mv chromium"
'

echo "Source directory is bootstrapped (at: $PWD), now clean it up"
echo "Use: https://github-vcf.devops.broadcom.net/vcf/photon-misc-scripts/tree/master/cleanup-chromium-src"
echo "Once done, run -> tar -I 'xz -9' -cpf $chromium_tarball src/"
popd # _tmp_

rm -rf depot_tools

popd # /tmp

echo -e "\n\n--- Done: tarballs are at $outputdir ---"
