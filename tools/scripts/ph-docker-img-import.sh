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

if [ "${ret}" != "${img_url}" ]; then
  docker rmi -f "${img_tag}" "${ph_builder_tag}"

  echo "Creating photon builder docker image ..."
  if ! docker import "${img_url}" "${img_tag}"; then
    echo "ERROR: docker import of ${img_url} docker image failed" 1>&2
    exit 1
  fi

  dbpath="/usr/lib/sysimage/rpm"
  if [ "$(rpm -E %{_db_backend})" = "sqlite" ] && [ "$(rpm -E %{_dbpath})" = "${dbpath}" ]; then
    echo "Host's rpm supports sqlite and RpmDB path is as expected"
    exit 0
  fi

  tmp_tag="$(mktemp -t photon_builder.XXXX -u | cut -d'/' -f3)"
  if ! docker run --name "${tmp_tag}" --net=host --privileged "${img_tag}" /bin/bash -c "tdnf install -y rpm" 1>/dev/null; then
    docker rmi -f "${img_tag}"
    echo "ERROR: docker run ${tmp_tag} failed" 1>&2
    exit 1
  fi

  if ! docker stop "${tmp_tag}" 1>/dev/null; then
    docker rm -f "${tmp_tag}"
    docker rmi -f "${img_tag}"
    echo "ERROR: docker stop ${tmp_tag} failed" 1>&2
    exit 1
  fi

  if ! docker commit "${tmp_tag}" "${ph_builder_tag}" 1>/dev/null; then
    docker rm -f "${tmp_tag}"
    docker rmi -f "${img_tag}"
    echo "ERROR: docker commit ${tmp_tag} failed" 1>&2
    exit 1
  fi

  if ! docker rm -f "${tmp_tag}" 1>/dev/null; then
    docker rmi -f "${img_tag}"
    echo "ERROR: docker rm -f ${tmp_tag} failed" 1>&2
    exit 1
  fi
fi

exit 0
