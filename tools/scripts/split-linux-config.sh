#!/bin/bash

#
# Usage <path-to-script> .config [<dir>]
#
# E.g.
#
#   $ ./split-linux-config.sh config_x86_64 /tmp/config_x86_64
#
#   output directory /tmp/config_x86_64 ...
#   24
#    General setup 24 -- 59
#     IRQ subsystem 59 -- 77
#    General setup 77 -- 91
#     Timers subsystem 91 -- 101
#   ...
#   ...
#     Kernel Testing and Coverage 6626 -- 6681
#    Kernel hacking 6681 -- 6682
#   Root Menu 6682 --
#
#   $ tree /tmp/config_x86_64
#   /tmp/config_x86_64
#   ├── cfg
#   └── Root Menu
#       ├── Binary Emulations
#       │   └── cfg
#       ├── Bluetooth device drivers
#       │   └── cfg
#       ├── Bus options (PCI etc.)
#       │   └── cfg
#       ├── Certificates for signature checking
#       │   └── cfg
#
#   ......

set -eu

TITLES=( "Root Menu" )
LINENOS=( 1 )

printm() {
   SPACES="$1"
   while [ $SPACES -gt 1 ]; do
      (( SPACES-- ))
      echo -n " "
   done
   echo -n "$2"
}

mkdirp() {
   if [ $# -eq 0 ]; then
      return
   fi
   local DIR="$1"
   local -a EXISTING
   shift
   if ! [ -d  "$DIR" ]; then
      shopt -s nullglob
      EXISTING=( * )
      shopt -u nullglob
      mkdir "$DIR"
      #ln -s "$DIR" ".sub.${#EXISTING[@]}"
   fi
   cd "$DIR"
   mkdirp "$@"
   cd ..
}

emit() {
   local START="$1"
   shift
   local END="$1"
   shift
   if [[ "$END" -eq "$START" ]]; then
      return
   fi
   [[ "$END" -gt "$START" ]]
   local CDIR
   printf -v CDIR "%s/" "$@"
   mkdirp "$@"
   local FNAME=".cfg.$(printf "%010d" $START)"
   tail "-n+$START" < "$CFG" | head "-n$(( END - START))" > "$CDIR/$FNAME"
   ln "$CDIR/$FNAME" "$FNAME"
}

process() {
   local LINE="$1"
   local TEXT="${LINE#*":# "}"
   local LINENO="${LINE:0:$(( ${#LINE} - ${#TEXT} - 3 ))}"
   TEXT="${TEXT//\//-}"
   if [[ "$TEXT" == "end of ${TITLES[-1]}" ]]; then
      local NEXT="$(( LINENO + 1))"
      echo "$NEXT"
      emit "${LINENOS[-1]}" "$NEXT" "${TITLES[@]}"
      unset TITLES[-1]
      unset LINENOS[-1]
      LINENOS[-1]="$NEXT"
      printm ${#TITLES[@]} "${TITLES[-1]} ${LINENOS[-1]} -- "
   else
      echo "$LINENO"
      emit "${LINENOS[-1]}" "$LINENO" "${TITLES[@]}"
      TITLES+=( "$TEXT" )
      LINENOS+=( "$LINENO" )
      printm ${#TITLES[@]} "${TITLES[-1]} ${LINENOS[-1]} -- "
   fi
}

finalize() {
   local -a DIRS
   local -a CFGS
   shopt -s nullglob
   DIRS=( * )
   CFGS=( .cfg.* )
   shopt -u nullglob
   if [ "${#DIRS[@]}" -gt 0 ]; then
      for d in "${DIRS[@]}"; do
         cd "$d"
         finalize
         cd ..
      done
   fi
   if [ "${#CFGS[@]}" -gt 0 ]; then
      for c in "${CFGS[@]}"; do
         cat "${CFGS[@]}" > cfg
      done
      rm "${CFGS[@]}"
   fi
}

if [ $# -gt 1 ]; then
   TDIR="$2"
else
   TDIR="$(mktemp -d /tmp/config-XXXXXX)"
fi

echo "output directory $TDIR ..." >&2

CFG="$(readlink -f "$1")"

pushd "$TDIR"
   while read -r ; do
      process "$REPLY"
   done < <(grep -En '^# ' < "$CFG" | grep -Fv '# CONFIG_')
   finalize
   diff -u "$CFG" cfg
popd
