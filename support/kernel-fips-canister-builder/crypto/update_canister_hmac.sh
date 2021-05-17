#! /bin/bash
#
# HMAC injection and canister sanity check script
#
# Copyright (C) 2020, 2021, VMware, Inc.
# Author: Alexey Makhalov <amakhalov@vmware.com>
#

set -e

# Canister obj file
INPUT_FILE=$1
# Generaged by gen_canister_relocs linker script
LD_SCRIPT=$2
# Canister image to measure
RAW_FILE=canister.raw
# File with HMAC digest
HMAC_FILE=canister.hmac
KEY="FIPS-PH4-VMW2020"

trap "exit 1" TERM
function abort() {
	echo $1
	kill -s TERM $$
}

function fail_if_found() {
  nm -u $INPUT_FILE | grep " U $1" > /dev/null && abort "Error: forbidden '$1' usage from the canister was found. Please fix it." ||:
}

# Canister sanity check:
# Canister should not contain several undefuned symbols,
# it should use alternatives from wrapper instad.
fail_if_found _cond_resched
fail_if_found __kmalloc
fail_if_found kmem_cache_alloc_trace
fail_if_found __list_add_valid
fail_if_found __mutex_init
fail_if_found mutex_lock
fail_if_found mutex_unlock
fail_if_found queue_work_on
fail_if_found latent_entropy

# Get sections list from linker script
sections=`grep ": {$" $LD_SCRIPT | cut -d " " -f3`
sfiles=""
for s in $sections;
do
  # Extrace section
  objcopy -O binary --only-section=$s ${INPUT_FILE} ${RAW_FILE}${s}
  sfiles="$sfiles ${RAW_FILE}${s}"
done
# Concatenate all extracted section into canister image
cat $sfiles > ${RAW_FILE}
rm $sfiles

# Measurement.
openssl dgst -sha256 -hmac $KEY -binary -out $HMAC_FILE $RAW_FILE

# Get file offset to the canister_hmac placeholder.
# It is in the .init.rodata.canister_info section with 0 offset.
# NOTE: readelf output can be truncated to .data.canist[...]
str=`eu-readelf -S ${INPUT_FILE} | grep init.rodata.canister_info`
test -z "$str" && exit 1
# return last word
#offset=0x${str##* }
# return 5th word
offset=0x$(echo $str | awk '{print $5}')
# HMAC digest injection
dd if=$HMAC_FILE of=${INPUT_FILE} seek=$((offset)) bs=1 count=32 conv=notrunc status=none

rm $RAW_FILE $HMAC_FILE

