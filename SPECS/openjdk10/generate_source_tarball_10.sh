tdnf install mercurial -y

if [[ $# -eq 0 ]] ; then
    echo 'Usage: generate_source_tarball.sh <Mercurial-Tag-Name> <openjdk version>'
    echo 'Example: generate_source_tarball.sh jdk-10+23 1.10.0.23'
    echo 'visit http://hg.openjdk.java.net/jdk10/jdk10/tags to use the appropriate tag name.'
    exit 0
fi
rm -rf openjdk-$2
hg clone http://hg.openjdk.java.net/jdk10/jdk10 -u $1 openjdk-$2
cd openjdk-$2
hg clone http://hg.openjdk.java.net/jdk10/jdk10/corba/ -u $1
hg clone http://hg.openjdk.java.net/jdk10/jdk10/hotspot/ -u $1
hg clone http://hg.openjdk.java.net/jdk10/jdk10/jaxp/ -u $1
hg clone http://hg.openjdk.java.net/jdk10/jdk10/jaxws/ -u $1
hg clone http://hg.openjdk.java.net//jdk10/jdk10/jdk/ -u $1
hg clone http://hg.openjdk.java.net/jdk10/jdk10/langtools/ -u $1
hg clone http://hg.openjdk.java.net/jdk10/jdk10/nashorn/ -u $1

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
