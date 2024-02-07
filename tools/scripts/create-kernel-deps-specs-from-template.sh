#!/bin/bash

script_dir="$(dirname ${BASH_SOURCE})"

if [ -d "$script_dir/SPECS" ]; then
  spec_dir="$(realpath $script_dir/SPECS)"
else
  spec_dir="$(realpath $script_dir/../../SPECS)"
fi

dist=".ph5"

create_specs() {
  if [ $# -ne 4 ]; then
    echo "ERROR: $FUNCNAME invalid args ..." 1>&2
    return 1
  fi

  local i=
  local kver_str="$1"
  local krel_str="$2"
  local ksubrel_str="$3"
  local pkg="$4"

  local kver_arr=()
  local krel_arr=()
  #local kver_arr=("6.1.75" "6.6.66" "6.8.88")
  #local krel_arr=("1" "2" "4")
  local sp=""

  local k_specs=($(grep -lrw "^Name:[[:space:]]*$pkg$" $spec_dir/linux/))

  for sp in ${k_specs[@]}; do
    kver_arr+=($(grep ^Version: $sp | awk '{print $2}'))
    krel_arr+=($(grep ^Release: $sp | awk '{print $2}' | tr -d -c 0-9))
  done

  for i in ${!kver_arr[@]}; do
    local kver="${kver_arr[$i]}"
    local krel="${krel_arr[$i]}${dist}"

    local a="$(echo $kver | cut -d. -f1)"
    local b="$(echo $kver | cut -d. -f2)"
    local c="$(echo $kver | cut -d. -f3)"
    [ -z "$c" ] && c="0"
    local d="${krel_arr[$i]}"

    local ksubrel=$(printf ".%02d%02d%03d%03d" "$a" "$b" "$c" "$d")

    for sp in ${specs[@]}; do
      local target_dir="$(dirname $sp)"
      local target_fn="$(basename -- ${sp} .spec)-${kver}.spec"
      echo "Now operating on '${kver}-${krel}' & ${target_fn} ..."
      sed -e "s|$kver_str|${kver}|" \
        -e "s|$krel_str|${krel}|" \
        -e "s|$ksubrel_str|${ksubrel}|" \
        ${sp} > ${target_dir}/${target_fn}
    done
  done
}

specs=(falco sysdig)
for s in ${!specs[@]}; do
  rm -f $spec_dir/${specs[$s]}/*.spec
  specs[$s]="$spec_dir/${specs[$s]}/${specs[$s]}.spec.in"
done

create_specs "%{KERNEL_VERSION}" "%{KERNEL_RELEASE}" "%{?kernelsubrelease}" "linux"

#specs=($(find $spec_dir -name "*.spec.in" | xargs -n1 grep -l -m1 %{LINUX_RT_KERNEL_VERSION}))
#create_specs "%{LINUX_RT_KERNEL_VERSION}" "%{LINUX_RT_KERNEL_RELEASE}" "%{?linuxrt_kernelsubrelease}" "linux-rt"
