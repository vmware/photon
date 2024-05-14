#!/bin/bash

script_dir="$(dirname ${BASH_SOURCE})"

if [ -d "$script_dir/SPECS" ]; then
  spec_dir="$(realpath $script_dir/SPECS)"
else
  spec_dir="$(realpath $script_dir/../../SPECS)"
fi

dist=".ph5"

declare -A kvers
declare -A krels

populate_kvers() {
  local i=""
  local sp=""

  for i in linux linux-esx linux-rt; do
    local k_specs=($(grep -lrw "^Name:[[:space:]]*$i$" $spec_dir/linux/))

    local x="$(echo $i | tr '-' '_')"
    for sp in ${k_specs[@]}; do
      if [[ -z "$KERNEL_VERSION" ]]; then
          kvers[$x]+="$(grep ^Version: $sp | awk '{print $2}')"
          krels[$x]+="$(grep ^Release: $sp | awk '{print $2}' | tr -d -c 0-9)"
      else
          local kver="${KERNEL_VERSION%%-*}"
          local rel="${KERNEL_VERSION##$kver-}"
          kvers[$x]+="$kver"
          krels[$x]+="${rel%%.ph*}"
      fi
    done
  done
}

create_specs() {
  if [ $# -ne 1 ]; then
    echo "ERROR: $FUNCNAME invalid args ..." 1>&2
    return 1
  fi

  local i=
  local kver_str="%{KERNEL_VERSION}"
  local krel_str="%{KERNEL_RELEASE}"
  local ksubrel_str="%{?kernelsubrelease}"

  local pkg="$1"

  local x="$(echo $pkg | tr '-' '_')"
  local kver_arr=${kvers[$x]}
  local krel_arr=${krels[$x]}
  #local kver_arr=("6.1.75" "6.6.66" "6.8.88")
  #local krel_arr=("1" "2" "4")
  local sp=""

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
      if echo $sp | grep -qE "iavf|i40e|ice"; then
        local kernel_flavour_macro="%{KERNEL_FLAVOUR}"
        local kernel_flavour="${pkg#linux}"
        local d_bname="$(basename -s .spec.in ${sp} | rev | cut -d- -f1 | rev)"

        local d_vers=()
        local tmp=(${d_info["$d_bname"]})
        local d_ver_macro="${tmp[${#tmp[@]}-1]}"

        for i in ${tmp[@]}; do
          [ "$i" != "$d_ver_macro" ] && d_vers+=("$i")
        done

        local d_ver=""
        for d_ver in ${d_vers[@]}; do
          local kernel_fn="$(basename -- ${sp} .spec.in)-${d_ver}-${kver}.spec"
          local target_fn=${pkg}-${kernel_fn#kernels-}
          #echo "Now operating on '${kver}-${krel}' & ${target_dir}/${target_fn} ..."
          sed -e "s|$kver_str|${kver}|" \
            -e "s|$krel_str|${krel}|" \
            -e "s|$ksubrel_str|${ksubrel}|" \
            -e "s|$d_ver_macro|${d_ver}|" \
            -e "s|$kernel_flavour_macro|${kernel_flavour}|" \
            ${sp} > ${target_dir}/${target_fn}
        done
      else
        local target_fn="$(basename -- ${sp} .spec.in)-${kver}.spec"
        #echo "Now operating on '${kver}-${krel}' & ${target_dir}/${target_fn} ..."
        sed -e "s|$kver_str|${kver}|" \
          -e "s|$krel_str|${krel}|" \
          -e "s|$ksubrel_str|${ksubrel}|" \
          ${sp} > ${target_dir}/${target_fn}
      fi
    done
  done
}

specs=(falco sysdig)
populate_kvers

echo "Creating ${specs[@]} specs ..."

for s in ${!specs[@]}; do
  rm -f $spec_dir/${specs[$s]}/*.spec
  specs[$s]="$spec_dir/${specs[$s]}/${specs[$s]}.spec.in"
done

create_specs "linux"

kernel_drivers_intel=()
for i in iavf i40e ice; do
  kernel_drivers_intel+=(kernels-drivers-intel-$i)
done

specs=(${kernel_drivers_intel[@]})

for s in ${!specs[@]}; do
  specs[$s]="$spec_dir/kernels-drivers-intel/${specs[$s]}.spec.in"
done
rm -f $spec_dir/kernels-drivers-intel/*.spec

declare -A d_info=()

d_info["ice"]="1.13.7 %{ICE_VERSION}"
d_info["iavf"]="4.9.5 %{IAVF_VERSION}"
d_info["i40e"]="2.22.18 %{I40E_VERSION}"

echo "Creating kernel drivers for linux ..."
create_specs "linux"

echo "Creating kernel drivers for linux-esx ..."
create_specs "linux-esx"

d_info["iavf"]="4.11.1 4.9.5 4.8.2 4.5.3 %{IAVF_VERSION}"
d_info["i40e"]="2.22.18 2.23.17 2.25.7 %{I40E_VERSION}"
d_info["ice"]="1.14.9 1.13.7 1.12.7 1.11.14 1.9.11 %{ICE_VERSION}"

echo "Creating kernel drivers for linux-rt ..."
create_specs "linux-rt"
