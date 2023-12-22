#! /bin/bash

# patch command does not support binary patches generated from git.
# If any of the patch does not apply for the same reason, fix the patch and copy it to SPECS/glibc/patches

set -e -x

if [ -z "$1" ]
then
  echo "Pass release as first argument"
  echo "Usage: ./generate-glibc-release-patches.sh 2.32"
  exit 1
fi

VERSION="${1}"
INCFILE="v${VERSION}.patches"

git clone https://sourceware.org/git/glibc.git
pushd glibc
git checkout release/${VERSION}/master
count="$(git rev-list glibc-${VERSION}..HEAD --count)"
git format-patch --binary --full-index -${count} HEAD
popd
rm -rf patches || true
mkdir -p patches
cp glibc/*.patch patches/

rm ${INCFILE} || true

pushd patches
seq=101
for patch in *.patch; do
    [ -e "$patch" ] || continue
    echo "Patch${seq}: ${patch}" >> ../${INCFILE}
    ((seq++))
done
popd

# Test for change in so versions
cp glibc/shlib-versions shlib-versions-latest

pushd glibc
git checkout tags/glibc-${VERSION} shlib-versions
popd

cp glibc/shlib-versions shlib-versions-release

diff shlib-versions-release shlib-versions-latest > /dev/null 2>&1
error=$?

if [ $error -eq 1 ]
then
   echo "shlib-versions file changed. Check for a patch which modifies the file and ensure it does not break a released so file"
   exit 1
fi