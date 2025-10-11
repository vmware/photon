#!/bin/bash

if [ $# -ne 2 ]; then
  echo "$0: ERROR: invalid number of args" 1>&2
  exit 1
fi

img_url=$1
img_tag=$2

ret="$(docker image inspect -f {{.Comment}} ${img_tag} 2>/dev/null)"
if [ $? -eq 0 ]; then
  ret="$(echo ${ret} | cut -d' ' -f3)"
else
  ret=""
fi

if [ "${ret}" != "${img_url}" ]; then
  docker rmi -f "${img_tag}"

  echo "Creating photon docker image ..."
  if ! docker import --message $"${img_url}" "${img_url}" "${img_tag}"; then
    echo "ERROR: docker import of ${img_url} docker image failed" 1>&2
    exit 1
  fi
fi

exit 0
