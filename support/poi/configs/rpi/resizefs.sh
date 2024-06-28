#!/bin/bash

set -e

SWAP_LABEL="PHOTON_SWAP"

DEV="$(findmnt -n -o SOURCE -M /)"
DEV="$(basename "$DEV")"

SYSFSP="/sys/class/block/$DEV"
SIZE="$(<"$SYSFSP/size")"
START="$(<"$SYSFSP/start")"
PARENT_DEV="$(basename "$(readlink -f "$SYSFSP/..")")"
PARENT_SIZE="$(<"$SYSFSP/../size")"
PARTNUM="$(<"$SYSFSP/partition")"

# Align to 1M (512 * 2048)
WANT_SIZE="$(( PARENT_SIZE / 2048 * 9 / 10 * 2048))"

get_partmap() {
  parted -m -s "/dev/$PARENT_DEV" unit s p
}

# Don't resize if we are alreay large enough
if [ "$SIZE" -ge "$WANT_SIZE" ]; then
  echo "root partition already resized, skip resizing" >&2
else
  # Workaround partition-in-use issue:
  # https://bugs.launchpad.net/ubuntu/+source/parted/+bug/1270203
  echo -e "yes\n$((WANT_SIZE + START - 1))" | \
  parted ---pretend-input-tty "/dev/$PARENT_DEV" unit s resizepart "$PARTNUM"
  partprobe "/dev/$PARENT_DEV"
  resize2fs "/dev/$DEV"
fi

if blkid -L "$SWAP_LABEL" >/dev/null ; then
  echo "swap partition already created, nothing to do">&2
  exit 0
fi

OLD_MAPF="$(mktemp)"
exec 3>"$OLD_MAPF"
exec 4<"$OLD_MAPF"
rm "$OLD_MAPF"

get_partmap >&3

parted -s "/dev/$PARENT_DEV" unit s mkpart primary linux-swap "$((WANT_SIZE + START))" 100%
partprobe "/dev/$PARENT_DEV"

# Find out the partition number we just created
# It should be in the format of
# "number":"begin":"end":"size":"filesystem-type":"partition-name":"flags-set";
IFS= mapfile -d: -t DIFF_MAP < <(join -v 2 - <(get_partmap) <&4)

# Sanity check: new partition should begin after root partition
if ! [ "${DIFF_MAP[1]%"s"}" -eq "${DIFF_MAP[1]%"s"}" ] ||
     [ "${DIFF_MAP[1]%"s"}" -lt "$((WANT_SIZE + START))" ]; then
  echo "Failed parsing partition map" >&2
  exit 1
fi

enable_swap() {
  mkswap "$1"
  swaplabel -L "$SWAP_LABEL" "$1"
  swapon "$1"
}

# Find out the block device name of the new partition,
# and enable swap on it.
shopt -s nullglob
for P in "$SYSFSP/../$PARENT_DEV"* ; do
  NEW_PART="$(<"$P/partition")" || continue
  [ "$NEW_PART" -eq "${DIFF_MAP[0]}" ] || continue
  enable_swap "/dev/$(basename "$P")"
  exit 0
done

echo "Failed to find new partition" >&2
exit 1
