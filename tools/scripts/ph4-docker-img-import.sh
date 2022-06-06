#!/bin/bash

if [ $# -ne 3 ]; then
  echo "$0: ERROR: invalid number of args" 1>&2
  exit 1
fi

img_url=$1
img_tag=$2
ph_builder_tag=$3

ret="$(docker image inspect -f {{.Comment}} ${img_tag} 2>/dev/null)"
if [ $? -eq 0 ]; then
  ret="$(echo ${ret} | cut -d' ' -f3)"
else
  ret=""
fi

photon_builder_dockerfile="support/package-builder/Dockerfile.photon_builder"

if [ "${ret}" != "${img_url}" ]; then
  docker rmi -f "${img_tag}" "${ph_builder_tag}"

  echo "Creating photon builder docker image ..."
  if ! docker import "${img_url}" "${img_tag}"; then
    echo "ERROR: docker import of ph3 docker image failed" 1>&2
    exit 1
  fi

  if ! docker build --tag "${ph_builder_tag}" -f ${photon_builder_dockerfile} . 1>/dev/null; then
    echo "ERROR: failed to build ${ph_builder_tag} docker image" 1>&2
    exit 1
  fi
fi

exit 0
