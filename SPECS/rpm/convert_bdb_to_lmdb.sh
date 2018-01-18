#!/bin/sh

#please see https://github.com/rpm-software-management/rpm/issues/281
#uses code from bdbexport.sh and lmdbimport.sh posted in the discussion. 

#Use: tool to convert bdb to lmdb and replace existing bdb.

#running rpm --rebuilddb is recommended after conversion
#for scenarios like docker, photon-micro etc
#rpm might not be installed as just rpm-libs is enough.
#a warning is issued in this case.

#not designed to run multiple times without doing manual
#maintenance in between (move backup folders etc)

LMDB=/var/lib/rpmdb-lmdb
BDB=/var/lib/rpm
DUMPDIR=DUMP

#bdb database file names
TAGS="
Packages
Name
Basenames
Group
Requirename
Providename
Conflictname
Obsoletename
Triggername
Dirnames
Installtid
Sigmd5
Sha1header
Filetriggername
Transfiletriggername
Recommendname
Suggestname
Supplementname
Enhancename
"

#backup existing bdb to /var/lib/rpm-bdb-backup
function backup_and_replace_rpmdb() {
  echo "backed up existing bdb to $BDB-bdb-backup"
  mv $BDB $BDB-bdb-backup
  mv $LMDB $BDB
  if [ -x /usr/bin/rpm ]; then
    rpm --rebuilddb
  else
    echo 'rpm binary not found. not running rebuilddb. please install rpm and run rpm --rebuilddb.'
  fi
}

function export_from_bdb() {

  rm -rf $DUMPDIR
  mkdir -p $DUMPDIR

  # --- export all the databases
  for TAG in $TAGS; do
    echo "-- $TAG --"
    [ -f $BDB/$TAG ] || continue
  # --- change from hash -> btree, including swabbing integer keys
    db_dump $BDB/$TAG | \
      sed -e's,^type=hash,type=btree,' -e'/^h_nelem=/d' -e'/^db_pagesize=/d' \
	-e's,^ \(..\)\(..\)\(..\)\(..\)$, \4\3\2\1,' \
	> $DUMPDIR/$TAG.btree
  done
}

function import_to_lmdb() {
  rm -rf $LMDB
  mkdir -p $LMDB

  # --- initialize the lmdb parameters (mapsize MUST be sufficiently large)
  cat << EOF | mdb_load $LMDB
VERSION=3
format=bytevalue
type=btree
mapsize=1048576000
maxreaders=64
HEADER=END
DATA=END
EOF

  # --- import the rpmdb dumps, creating empty indices (unused on RHEL7) as needed
  for TAG in $TAGS; do
    echo "-- $TAG --"
    case $TAG in
    Enhance*|Filetrigger*|Recommend*|Suggest*|Supplement*|Transfiletrigge*)
	mdb_load -s $TAG -T $LMDB < /dev/null
	;;
    *)
	mdb_load -f $DUMPDIR/$TAG.btree -s $TAG $LMDB
	;;
    esac
  done

  mdb_stat -a $LMDB
}

function make_lmdb_from_bdb() {
  export_from_bdb
  import_to_lmdb
}

#check and convert
function check_and_convert() {
  if [ ! -x /usr/bin/db_dump ]; then
    echo 'libdb-utils is required to do bdb export. please install libdb-utils and try again.'
    return 1
  fi
  echo 'checking if rpmdb needs conversion'
  if [ -f $BDB/Packages ]; then
    echo 'making lmdb from mdb'
    make_lmdb_from_bdb
    echo 'backing up and replacing bdb with lmdb'
    backup_and_replace_rpmdb
  fi
}

#convert if required.
check_and_convert
