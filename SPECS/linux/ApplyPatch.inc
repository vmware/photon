#
# Copyright (C) 2022 VMware, Inc. All Rights Reserved.
#

# get all patch names from spec
patches=($(grep -E "^Patch[0-9]+:" %{_specdir}/%{name}.spec | awk '{print $2}'))

# get the corresponding patch number from spec
patch_nums=($(grep -E "^Patch[0-9]+:" %{_specdir}/%{name}.spec | cut -d':' -f1 | sed 's/[^0-9]*//g'))

# a dictionary with patch_num -> patch_name mapping
# Example, if spec has:
# Patch0: example0.patch
# Patch123: example123.patch
# patch_dict[0] -> example0.patch
# patch_dict[123] -> example123.patch

declare -A patch_dict

idx=0
for pfn in ${patches[@]}; do
  patch_dict[${patch_nums[${idx}]}]="$(basename ${pfn})"
  idx=$((idx+1))
done

ApplyPatch()
{
  local start=${1:-1}
  local end=${2:-1}

  if [ ${start} -lt 0 ] || [ ${end} -lt 0 ]; then
    echo "Invalid argument to ApplyPatch" 1>&2
    exit 1
  fi

  while [ ${start} -le ${end} ]; do
    if [ -v patch_dict[${start}] ]; then
      echo "Patch #$start ($(basename ${patch_dict[${start}]})):"
      /bin/patch --no-backup-if-mismatch -p1 --fuzz=0 < %{_sourcedir}/${patch_dict[${start}]}
    fi
    start=$((start+1))
  done
}
