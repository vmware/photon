path=/var/run/tdnf-updateinfo.txt

if [ -f "$path" ]; then
    cat $path
else
    echo "tdnf update info not available yet!"
fi
