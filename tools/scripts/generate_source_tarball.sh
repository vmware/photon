#!/bin/bash

if [[ $# -ne 2 ]] ; then
  echo 'Usage: generate_source_tarball.sh <Mercurial-Tag-Name> <openjdk version>'
  echo 'Example: generate_source_tarball.sh jdk8u152-b16 1.8.0.152'
  echo 'Visit http://hg.openjdk.java.net/jdk8u/jdk8u/tags to use the appropriate tag name.'
  exit 0
fi

rm -rf openjdk-$2
hg clone http://hg.openjdk.java.net/jdk8u/jdk8u -u $1 openjdk-$2

pushd openjdk-$2
hg clone http://hg.openjdk.java.net/jdk8u/jdk8u/corba/ -u $1
hg clone http://hg.openjdk.java.net/jdk8u/jdk8u/hotspot/ -u $1
hg clone http://hg.openjdk.java.net/jdk8u/jdk8u/jaxp/ -u $1
hg clone http://hg.openjdk.java.net/jdk8u/jdk8u/jaxws/ -u $1
hg clone http://hg.openjdk.java.net/jdk8u/jdk8u/jdk/ -u $1
hg clone http://hg.openjdk.java.net/jdk8u/jdk8u/langtools/ -u $1
hg clone http://hg.openjdk.java.net/jdk8u/jdk8u/nashorn/ -u $1

rm -r .hg \
      corba/.hg \
      hotspot/.hg \
      jaxp/.hg \
      jaxws/.hg \
      jdk/.hg \
      langtools/.hg \
      nashorn/.hg
popd

tar -czf openjdk-$2.tar.gz openjdk-$2
chmod 644 openjdk-$2.tar.gz

echo 'source tarball openjdk-$2.tar.gz successfully created!'
