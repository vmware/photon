#! /bin/bash

# Dist tag must present in Release:
function check-for-dist-tag()
{
  cat $1 | grep "Release:" | grep "%{?dist}" > /dev/null
  if [ "$?" -ne 0 ];then
    echo "ERROR in $1: Release field doesn't contain %{?dist} tag"
    cat $1 | grep "Release:"
    exit 1
  fi
}

# Check for Version-Release matching top entry from the Changelog
function check-for-correct-version()
{
  versions=`sed -e '1,/%changelog/d' $1 | grep '<' | grep '>' | grep '*' | cut -f 2 -d '>'`;
  latest_version_in_changelog=`echo $versions | cut -d ' ' -f 1`
  version=`cat $1 | grep Version: | cut -f 2 -d ':'  | sed 's/ //g'  | sed '1!d'`;
  sub_version=`cat $1 | grep Release: | cut -f 2 -d ':' | cut -f 1 -d '%' | sed 's/ //g' | tr -d ' '`
  s=`echo ${sub_version//[[:blank:]]/}`
  v=`echo ${version//[[:blank:]]/}`
  full_version=${v}-${s};
  if [ "${latest_version_in_changelog}" != "${full_version}" ]; then
    echo "ERROR in $1: Top changelog entry version ${latest_version_in_changelog} does NOT MATCH package version ${full_version}"
    echo "Please update %changelog or Version,Release: in $1 to make them match each other"
    exit 1
  fi
}

# Changelog should have correct dates
function check-for-bogus-dates()
{
  local IFS=$'\n'
  for entry in `sed -e '1,/%changelog/d' $i | grep '<' | grep '>' | grep '*' | sed 's/^*//g' | sed 's/ \+/ /g'` ; do
    IFS=$' ' read D m d y s <<< $entry
    day=`date --date "$m $d $y" +%a`
    if [ "${D}" != "${day}" ]; then
      echo "ERROR in $1: bogus date in $entry"
      echo "$m $d $y is $day"
      exit 1
    fi
  done
}

# No trailing spaces
function check-for-trailing-spaces()
{
  grep -e " $" $1
  if [ $? -eq 0 ] ; then
      echo "ERROR in $1: trailing spaces detected"
      exit 1
  fi
}

# Do not use ./configure
function check-for-configure()
{
  grep -e "./configure" $1
  if [ $? -eq 0 ] ; then
      echo "ERROR in $1: use %configure instead of ./configure"
      exit 1
  fi
}

# All BuildRequires should on the top
function check-for-buildrequires()
{
  sed -e '1,/%description/d' $1 | grep -e "^BuildRequires"
  if [ $? -eq 0 ] ; then
      echo "ERROR in $1: BuildRequires in subpackages detected."
      echo "Move all BuildRequires to the top"
      exit 1
  fi
}

SPECS=`git diff --name-only $1 @ | grep -e "SPECS/.*.spec$"`
for i in `echo $SPECS`;
do
  echo Analyzing $i ...
  if [ ! -f $i ]; then
     echo "$i is removed by the current changeset."
  else
    check-for-dist-tag $i
    check-for-correct-version $i
    check-for-bogus-dates $i
    check-for-trailing-spaces $i
    check-for-configure $i
    check-for-buildrequires $i
  fi
done
