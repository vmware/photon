#!/bin/bash
# -*- mode: shell-script; indent-tabs-mode: true; tab-width: 4; -*-

# This script turns sysuser.d files into scriptlets mandated by Fedora
# packaging guidelines. The general idea is to define users using the
# declarative syntax but to turn this into traditional scriptlets.

user() {
  local user="$1"
  local uid="$2"
  local desc="$3"
  local group="$4"
  local home="$5"
  local shell="$6"

  [ "$desc" = '-' ] && desc=
  { [ "$home" = '-' ] || [ "$home" = '' ]; } && home=/
  { [ "$shell" = '-' ] || [ "$shell" = '' ]; } && shell=/usr/sbin/nologin

  if [ "$uid" = '-' ] || [ "$uid" = '' ]; then
    cat <<EOF
getent passwd '$user' >/dev/null || \\
  useradd -r -g '$group' -d '$home' -s '$shell' -c '$desc' '$user' || :
EOF
  else
    cat <<EOF
if ! getent passwd '$user' >/dev/null; then
  if ! getent passwd '$uid' >/dev/null; then
    useradd -r -u '$uid' -g '$group' -d '$home' -s '$shell' -c '$desc' '$user' || :
  else
    useradd -r -g '$group' -d '$home' -s '$shell' -c '$desc' '$user' || :
  fi
fi
EOF
  fi
}

group() {
  local group="$1"
  local gid="$2"

  if [ "$gid" = '-' ]; then
    cat <<EOF
getent group '$group' >/dev/null || groupadd -r '$group' || :
EOF
  else
    cat <<EOF
getent group '$group' >/dev/null || groupadd -f -g '$gid' -r '$group' || :
EOF
  fi
}

usermod() {
  local user="$1"
  local group="$2"

  cat <<EOF
if getent group '$group' >/dev/null; then
  usermod -a -G '$group' '$user' || :
fi
EOF
}

parse() {
  local line=""
  while read -r line || [ -n "$line" ] ; do
    { [ "${line:0:1}" = '#' ] || [ "${line:0:1}" = ';' ]; } && continue
    line="${line## *}"
    [ -z "$line" ] && continue
    eval "arr=( $line )"
    case "${arr[0]}" in
      ('u')
        if [[ "${arr[2]}" == *":"* ]]; then
          user "${arr[1]}" "${arr[2]%:*}" "${arr[3]}" "${arr[2]#*:}" "${arr[4]}" "${arr[5]}"
        else
          group "${arr[1]}" "${arr[2]}"
          user "${arr[1]}" "${arr[2]}" "${arr[3]}" "${arr[1]}" "${arr[4]}" "${arr[5]}"
        fi
        ;;
      ('g')
        group "${arr[1]}" "${arr[2]}"
        ;;
      ('m')
        group "${arr[2]}" "-"
        user "${arr[1]}" "-" "" "${arr[1]}" "" ""
        usermod "${arr[1]}" "${arr[2]}"
        ;;
    esac
  done
}

for fn in "$@"; do
  [ -e "$fn" ] || continue
  echo "# generated from $(basename "$fn")"
  parse <"$fn"
done
