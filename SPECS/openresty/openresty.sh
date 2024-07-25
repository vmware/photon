#!/bin/bash

orprefix="@@ORPREFIX@@"
[ -d "${orprefix}/bin" ] && PATH="${PATH}:${orprefix}/bin"
[ -d "${orprefix}/nginx/sbin" ] && PATH="${PATH}:${orprefix}/nginx/sbin"
export PATH
