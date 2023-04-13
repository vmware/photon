#!/bin/bash

set -e

if [ $# -ne 2 ]; then
  echo -e "Invalid args\nExample: $0 <old-ver> <new-ver>" 1>&2
  exit 1
fi

for tool in jq sed; do
  if ! command -v $tool &> /dev/null; then
    echo "ERROR: $tool not found, it's a must have" 1>&2
    exit 1
  fi
done

OLD_VER="$1"
NEW_VER="$2"

majver="$(echo ${NEW_VER} | cut -d. -f1)"
topdir="$(git rev-parse --show-toplevel)"

cd $topdir

SPECS=(photon-release photon-repos minimal basic)
for specFile in ${SPECS[@]}; do
  echo -e "\nUpdating ${specFile} packages ..."
  fn="SPECS/${specFile}/${specFile}.spec"
  # Update %version
  sed -i -e "s/^\(Version:[[:space:]]*\)[^[:space:]].*$/\1${NEW_VER}/" $fn

  # Update %release
  sed -i -e "s/^\(Release:[[:space:]]*\)[^[:space:]]*%\(.*\)$/\10%\2/" $fn
  ./tools/scripts/lazyspec.pl --message "Update to v${NEW_VER}" $fn
done

fn="SPECS/rpm-ostree/mkostreerepo"
echo -e "\nUpdating $fn ..."
sed -i "s/PHOTON_VERSION=.*/PHOTON_VERSION=\"${NEW_VER}\"/g" $fn
fn="SPECS/rpm-ostree/rpm-ostree.spec"
./tools/scripts/lazyspec.pl --message "Update dist tag" $fn

echo -e "\nUpdating dockerfiles under support/dockerfiles/k8s-docker-images ..."
sed -i "s/k8s-base-image:${OLD_VER}/k8s-base-image:${NEW_VER}/g" support/dockerfiles/k8s-docker-images/Dockerfile.*

fn="build-config.json"
echo -e "\nUpdating $fn ..."
jq ".\"photon-build-param\".\"photon-dist-tag\"=\".ph${majver}\"" $fn > $fn.tmp
mv $fn.tmp $fn
jq ".\"photon-build-param\".\"photon-release-version\"=\"${NEW_VER}\"" $fn > $fn.tmp
mv $fn.tmp $fn

LICENSES=($topdir/LICENSE.md $topdir/SPECS/LICENSE.md)
cur_year="$(date +'%Y')"
for fn in ${LICENSES[@]}; do
  echo -e "\nUpdating ${fn} ..."
  sed -i "s/VMware, Inc. 2014-20.*$/VMware, Inc. 2014-${cur_year}/g" "$fn"
done

README=(${topdir}/README.md)
sed -i "s/${OLD_VER}/${NEW_VER}/g" "$README"

prompt() {
  local yn=""
  local question="$1"

  while true; do
    read -p "$question, agree? [y/n] " yn
    case $yn in
      y ) return;;
      * ) echo "Please answer y or n";;
    esac
  done
}

prompts=(
"You need to update support/image-builder/iso/BUILD_DVD/isolinux/splash.png"
"You need to check SPECS/photon-installer for old version entries"
"Check the git diff thoroughly after running this script & then push the changes for review"
)

for p in "${prompts[@]}"; do
  echo -e "\n"
  prompt "$p"
done
