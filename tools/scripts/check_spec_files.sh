#! /bin/bash

function check-for-header()
{
  local n=

  for n in Summary Name Version Release License Group Vendor Distribution ; do
    if ! grep -qe "^$n:" $1; then
      echo "ERROR in $1: $n: must present in the header"
      exit 1
    fi
  done
}

# Dist tag must present in Release:
function check-for-dist-tag()
{
  if ! grep "Release:" $1 | grep -q "%{?dist}"; then
    echo "ERROR in $1: Release field doesn't contain %{?dist} tag"
    grep "Release:" $1
    exit 1
  fi
}

# Check for Version-Release matching top entry from the Changelog
function check-for-correct-version()
{
  local versions=`sed -e '1,/%changelog/d' $1 | grep '<' | grep '>' | grep '*' | cut -f 2 -d '>'`;
  local latest_version_in_changelog=`echo $versions | cut -d ' ' -f 1`
  local version=`grep Version: $1 | cut -f 2 -d ':'  | sed 's/ //g'  | sed '1!d'`;
  local sub_version=`grep Release: $1 | cut -f 2 -d ':' | cut -f 1 -d '%' | sed 's/ //g' | tr -d ' '`
  local s=`echo ${sub_version//[[:blank:]]/}`
  local v=`echo ${version//[[:blank:]]/}`
  local full_version=${v}-${s};

  if ! grep -q dialogsubversion $1; then
     local dialogsubversion=`grep dialogsubversion $1 | grep %global | cut -d ' ' -f 3 | sed 's/ //g' | tr -d ' '`
     local full_version=${v}-${s}${dialogsubversion}
  fi
  if [ "${latest_version_in_changelog}" != "${full_version}" ]; then
    echo "ERROR in $1: Top changelog entry version ${latest_version_in_changelog} does NOT MATCH package version ${full_version}"
    echo "Please update %changelog or Version,Release: in $1 to make them match each other"
    exit 1
  fi
}

# Changelog should have:
# - correct day of week for the date
# - descending chronological order
# - whitespaces are ignored while validating dates
function check-for-bogus-dates()
{
  local D=''
  local m=''
  local d=''
  local y=''
  local epoch_seconds=''
  local prev_epoch_seconds=$(date +%s)

  while read D m d y; do
    day=$(date --date="$m $d $y" '+%a')
    if [ "${D}" != "${day}" ]; then
      echo "ERROR in $1: bogus date $m $d $y found - actual day is $day, but found $D"
      exit 1
    fi
    epoch_seconds=$(date --date "$m $d $y" +%s)
    if [ $prev_epoch_seconds -lt $epoch_seconds ]; then
      echo "ERROR in $1: %changelog not in descending chronological order"
      echo "Date validation failed at $D $m $d $y"
      exit 1
    fi
    prev_epoch_seconds=$epoch_seconds
  done <<< "$(sed -e '1,/%changelog/d' "$1" | grep '^\*' | awk '{printf "%s %s %02d %04d\n", $2, $3, $4, $5}')"
}

# No trailing spaces
function check-for-trailing-spaces()
{
  if grep -qe " $" $1; then
    echo "ERROR in $1: trailing spaces detected"
    exit 1
  fi
}

# Use %configure instead of ./configure
# De not redefine standard paths parameters
function check-for-configure()
{
  local param=

  if grep -e "^\./configure" $1; then
    echo "ERROR in $1: use %configure instead of ./configure"
    exit 1
  fi

  grep -q "%configure" $1 || return

  if grep -Pzo ".*\\\\(\n)%configure.*" $1; then
    echo
    echo "Trailing backslash before %configure found. Please use export instead"
    exit 1
  fi

  for param in prefix exec-prefix bindir sbindir libdir includedir sysconfdir datadir libexecdir sharedstatedir mandir infodir localstatedir; do
    if grep -e "\(configure\|^\)[ \t]\+--$param=%{_$param}" $1; then
      echo "ERROR in $1: --$param can be ommited when using %configure"
      exit 1
    fi
  done
}

# All BuildRequires should on the top
function check-for-buildrequires()
{
  if sed -e '1,/%description/d' $1 | grep -e "^BuildRequires"; then
    echo "ERROR in $1: BuildRequires in subpackages detected."
    echo "Move all BuildRequires to the top"
    exit 1
  fi
}

if [ -z "$(git diff --name-only HEAD --)" ] ; then
	SPECS=`git diff --name-only @~ | grep -e "SPECS/.*.spec$"`
else
	SPECS=`git diff --name-only | grep -e "SPECS/.*.spec$"`
fi
for i in `echo $SPECS`; do
  echo Analyzing $i ...
  if [ ! -f $i ]; then
     echo "$i is removed by the current changeset."
  else
    check-for-header $i
    check-for-dist-tag $i
    check-for-correct-version $i
    check-for-bogus-dates $i
    check-for-trailing-spaces $i
    check-for-configure $i
    check-for-buildrequires $i
  fi
done
