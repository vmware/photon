tdnf install mercurial -y

if [[ $# -eq 0 ]] ; then
    echo 'Usage: generate_source_tarball_11.sh <Mercurial-Tag-Name> <openjdk version>'
    echo 'Example: generate_source_tarball_11.sh jdk-11+23 11.0.23'
    echo 'visit http://hg.openjdk.java.net/jdk-updates/jdk11u/tags to use the appropriate tag name.'
    exit 0
fi
rm -rf openjdk-$2
hg clone http://hg.openjdk.java.net/jdk-updates/jdk11u -u $1 openjdk-$2
cd openjdk-$2
hg clone http://hg.openjdk.java.net/jdk-updates/jdk11u/corba/ -u $1
hg clone http://hg.openjdk.java.net/jdk-updates/jdk11u/hotspot/ -u $1
hg clone http://hg.openjdk.java.net/jdk-updates/jdk11u/jaxp/ -u $1
hg clone http://hg.openjdk.java.net/jdk-updates/jdk11u/jaxws/ -u $1
hg clone http://hg.openjdk.java.net/jdk-updates/jdk11u/jdk/ -u $1
hg clone http://hg.openjdk.java.net/jdk-updates/jdk11u/langtools/ -u $1
hg clone http://hg.openjdk.java.net/jdk-updates/jdk11u/nashorn/ -u $1

rm -r .hg
rm -r corba/.hg
rm -r hotspot/.hg 
rm -r jaxp/.hg
rm -r jaxws/.hg
rm -r jdk/.hg
rm -r langtools/.hg
rm -r nashorn/.hg
cd ..

tar -cvzf openjdk-$2.tar.gz openjdk-$2
chmod 644 openjdk-$2.tar.gz

echo 'source tarball openjdk-$2.tar.gz successfully created!' 
