#!/bin/bash

dist=".ph5"

declare -A kvers
declare -A krels
declare -A build_for
declare -A specs_map=(
[linux_specs]="linux linux-esx linux-rt"
[kernel_drivers_intel]="kernels-drivers-intel-iavf kernels-drivers-intel-i40e kernels-drivers-intel-ice"
[other_specs]="sysdig falco"
)


# _______________________________________________________________________________
# |                           Kernel - Intel Driver Map                         |
# |_____________________________________________________________________________|
# |	 |             v6.6 	           |     v6.1                           |
# |______|_________________________________|____________________________________|
# | ice  | "4.19.9" [linux,linux-{esx,rt}] |  "1.14.9" [linux-rt]               |
# |      |                                 |  "1.13.7" [linux,linux-{esx,rt}]   |
# |      |                                 |  "1.12.7" [linux-rt]               |
# |      |                                 |  "1.11.14"[linux-rt]               |
# |      |                                 |  "1.9.11" [linux-rt]               |
# |______|_________________________________|____________________________________|
# | iavf | "4.11.1" [linux,linux-{esx,rt}] |  "4.11.1" [linux-rt]               |
# |      |                                 |  "4.9.5"  [linux,linux-{esx,rt}]   |
# |      |                                 |  "4.8.2"  [linux-rt]               |
# |      |                                 |  "4.5.3"  [linux-rt]		|
# |______|_________________________________|____________________________________|
# | i40e | "2.25.7" [linux,linux-{esx,rt}] |  "2.25.7" [linux-rt]               |
# |      |                                 |  "2.23.17"[linux-rt]               |
# |      |                                 |  "2.22.18"[linux,linux-{esx,rt}]	|
# |______|_________________________________|____________________________________|
#
# Note: While adding/removing any version from any of the given drivers,
#       Please update above table and carefully update all the references
#       of i40e/ice/iavf read-only array
declare -ra i40e=("2.25.7" "2.23.17" "2.22.18")
declare -ra ice=("1.14.9" "1.13.7" "1.12.7" "1.11.14" "1.9.11")
declare -ra iavf=("4.11.1" "4.9.5" "4.8.2" "4.5.3")

# Note: Composite Key speretated by ':' is being used as per below nomenclature
# [KernelVersion:DriverVersion:KernelFlavour]
declare -rA kernel_driver_map=(
 [v6.6:i40e:linux]="${i40e[0]}"
 [v6.1:i40e:linux]="${i40e[2]}"
 [v6.6:ice:linux]="${ice[0]}"
 [v6.1:ice:linux]="${ice[1]}"
 [v6.6:iavf:linux]="${iavf[0]}"
 [v6.1:iavf:linux]="${iavf[1]}"

 [v6.6:i40e:linux-esx]="${i40e[0]}"
 [v6.1:i40e:linux-esx]="${i40e[2]}"
 [v6.6:ice:linux-esx]="${ice[0]}"
 [v6.1:ice:linux-esx]="${ice[1]}"
 [v6.6:iavf:linux-esx]="${iavf[0]}"
 [v6.1:iavf:linux-esx]="${iavf[1]}"

 [v6.6:i40e:linux-rt]="${i40e[0]}"
 [v6.1:i40e:linux-rt]="${i40e[@]}"
 [v6.6:ice:linux-rt]="${ice[0]}"
 [v6.1:ice:linux-rt]="${ice[@]}"
 [v6.6:iavf:linux-rt]="${iavf[0]}"
 [v6.1:iavf:linux-rt]="${iavf[@]}"
)

populate_kvers() {
  local i=""
  local sp=""

  for i in ${specs_map["linux_specs"]}; do
    local k_specs=( $(find -L $@ -type f -path "*/${i}.spec") )

    local x="$(echo $i | tr '-' '_')"

    for sp in ${k_specs[@]}; do
      if [[ -z "$KERNEL_VERSION" ]]; then
          kvers[$x]+="$(grep ^Version: $sp | awk '{print $2}') "
          krels[$x]+="$(grep ^Release: $sp | awk '{print $2}' | tr -d -c 0-9) "
      else
          local kver="${KERNEL_VERSION%%-*}"
          local rel="${KERNEL_VERSION##$kver-}"
          kvers[$x]+="$kver "
          krels[$x]+="${rel%%.ph*} "
      fi

      # Get the build_for value
      build_for_value="$(grep -E '^\s*%global\s+build_for' "$sp" | sed -E 's/^\s*%global\s+build_for\s+//; s/^\s*|\s*$//g; s/!\s*\(\s*/!(/; s/\s*\),/),/g; s/\s*,\s*/,/g')"

      # Check if build_for_value is empty and append accordingly
      if [[ -z "$build_for_value" ]]; then
          build_for[$x]+="all "  # Append "all" to the array
      else
          build_for[$x]+="$build_for_value "  # Append the found value
      fi
    done
    kvers[$x]=$(echo "${kvers[$x]}" | sed 's/[[:space:]]*$//')
  done
}

# Trim down the input driver versions as per
# "kernel - Intel Driver Map"
get_kernel_compatible_drivers() {
  local kernel_version="$1"
  local driver_name="$2"
  local -n driver_versions="$3"
  local kernel_flavour="linux$4"
  local kd_map_key="v$(echo "$kernel_version" | cut -d '.' -f1,2):${driver_name}:${kernel_flavour}"
  local valid_driver_versions=(${kernel_driver_map["$kd_map_key"]})
  local temp=()
  for (( i=0; i<${#driver_versions[@]}; i++ )); do
    for t in "${valid_driver_versions[@]}"; do
      if [[ "$t" == "${driver_versions[$i]}" ]]; then
        temp+=("$t")
        break
      fi
    done
  done
  driver_versions=("${temp[@]}")
}

create_specs() {
  if [ $# -lt 1 ]; then
    echo "ERROR: $FUNCNAME invalid args ..." 1>&2
    return 1
  fi

  local i=
  local kver_str="%{KERNEL_VERSION}"
  local krel_str="%{KERNEL_RELEASE}"
  local ksubrel_str="%{?kernelsubrelease}"

  local pkg="$1"
  local oot_experimental="$2"

  local x="$(echo $pkg | tr '-' '_')"
  local kver_arr=(${kvers[$x]})
  local krel_arr=(${krels[$x]})
  local build_for_arr=(${build_for[$x]})
  #local kver_arr=("6.1.75" "6.6.66" "6.8.88")
  #local krel_arr=("1" "2" "4")
  local sp=""

  for i in ${!kver_arr[@]}; do
    local kver="${kver_arr[$i]}"
    local krel="${krel_arr[$i]}${dist}"
    local build_for_value="${build_for_arr[$i]}"

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

        if [[ -z "$oot_experimental" ]]; then
          get_kernel_compatible_drivers "$kver" "$d_bname" d_vers "$kernel_flavour"
          if [[ ${#d_vers[@]} -eq 0 ]]; then
            echo "ERROR: For kernel version:$kver, NO valid version of $d_bname found!!" 1>&2
            return 1
          fi
        fi

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
            -e "s|"%{BUILD_FOR}"|${build_for_value}|" \
            ${sp} > ${target_dir}/${target_fn}
        done
      else
        local target_fn="$(basename -- ${sp} .spec.in)-${kver}.spec"
        #echo "Now operating on '${kver}-${krel}' & ${target_dir}/${target_fn} ..."
        sed -e "s|$kver_str|${kver}|" \
          -e "s|$krel_str|${krel}|" \
          -e "s|$ksubrel_str|${ksubrel}|" \
          -e "s|"%{BUILD_FOR}"|${build_for_value}|" \
          ${sp} > ${target_dir}/${target_fn}
      fi
    done
  done
}

populate_kvers $@

specs=(${specs_map["other_specs"]})

echo "Creating ${specs[@]} specs ..."

for s in ${!specs[@]}; do
  find -L $@ -type f -path "*/${specs[$s]}/*.spec" -delete
  specs[$s]="$(find -L $@ -type f -name ${specs[$s]}.spec.in)"
done

create_specs "linux"

kernel_drivers_intel=()
specs=(${specs_map["kernel_drivers_intel"]})

for s in ${!specs[@]}; do
  specs[$s]="$(find -L $@ -type f -name ${specs[$s]}.spec.in )"
done
find -L $@ -type f -path "*/kernels-drivers-intel/*.spec" -delete

declare -A d_info=()

d_info["ice"]="${ice[@]: 0: 2} %{PKG_VERSION}"
d_info["iavf"]="${iavf[@]: 0: 2} %{PKG_VERSION}"
d_info["i40e"]="${i40e[0]} ${i40e[2]} %{PKG_VERSION}"

echo "Creating kernel drivers for linux ..."
create_specs "linux"

echo "Creating kernel drivers for linux-esx ..."
create_specs "linux-esx"

d_info["iavf"]="${iavf[@]} %{PKG_VERSION}"
d_info["i40e"]="${i40e[@]} %{PKG_VERSION}"
d_info["ice"]="${ice[@]} %{PKG_VERSION}"

echo "Creating kernel drivers for linux-rt ..."
create_specs "linux-rt"
