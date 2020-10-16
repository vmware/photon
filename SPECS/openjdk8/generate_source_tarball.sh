#!/bin/bash

set -x

if [ $# -ne 2 ]; then
    echo 'Usage: generate_source_tarball.sh <Mercurial-Tag-Name> <openjdk version>'
    echo 'Example: generate_source_tarball.sh jdk8u152-b16 1.8.0.152'
    echo 'visit http://hg.openjdk.java.net/jdk8u/jdk8u/tags to use the appropriate tag name.'
    exit 1
fi

if [[ "$1" = *aarch64* ]]; then
  url="http://hg.openjdk.java.net/aarch64-port/jdk8u"
  tarball_name="$1.tar.gz"
  clone_dir="openjdk-aarch64-jdk8u-$1"
else
  url="http://hg.openjdk.java.net/jdk8u/jdk8u/"
  tarball_name="openjdk-$2.tar.gz"
  clone_dir="openjdk-$2"
fi

rm -rf "${clone_dir}" && mkdir -p "${clone_dir}"
hg clone "${url}" -u $1 "${clone_dir}"
cd "${clone_dir}"

for i in corba hotspot jaxp jaxws jdk langtools nashorn; do
  hg clone "${url}/${i}" -u $1
  rm -rf .hg "${i}/.hg"
done

cd ..

tar -czf "${tarball_name}" "${clone_dir}" && chmod 644 "${tarball_name}"

echo "source tarball ${tarball_name} successfully created!"
