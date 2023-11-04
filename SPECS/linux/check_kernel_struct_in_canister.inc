#!/bin/sh
file_name="objs"
awk -i inplace '!seen[$0]++'  "$file_name"
name_lock=""
name_tsk=""
ret=0
while read crypto_obj; do
  touch ${crypto_obj}-struct
  gdb crypto/${crypto_obj} -q -ex="set pagination off" -ex="info types" -ex q | tail -n +2 > ${crypto_obj}-types
  while read line; do
       if [[ $line =~ ^[0-9]*:[[:space:]]*.*struct|union ]]; then
           echo $line | awk '{print "struct "$NF}' | sed -r 's/;+$//' >> ${crypto_obj}-struct
       fi
  done <${crypto_obj}-types
  count=$(cat ${crypto_obj}-struct | wc -l)
  echo "List of strctures in ${crypto_obj} is ${count}"
  str=$(awk /task_struct/ ${crypto_obj}-struct)
  if [ ! -z "$str" ]; then
     name_tsk="${name_tsk} ${crypto_obj}"
  fi
  str=$(awk /spinlock\|mutex/ ${crypto_obj}-struct)
  if [ ! -z "$str" ]; then
     name_lock="${name_lock} ${crypto_obj}"
  fi
  rm -f ${crypto_obj}-types
  rm -f ${crypto_obj}-struct
done<${file_name}
if [ ! -z "$name_tsk" ]; then
   echo "$name_tsk contains task_struct!!!!"
   ret=1
fi
if [ ! -z "$name_lock" ]; then
   echo "$name_lock contains spinlock or mutex!!!!"
   ret=1
fi
exit $ret
