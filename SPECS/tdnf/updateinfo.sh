path=/var/cache/tdnf/cached-updateinfo.txt

if [ -f "$path" ]; then
    grep -q -E 'Security|Bugfix|Enhancement' $path || exit 0
    echo; cat $path; echo "Run 'tdnf updateinfo info' to see the details."
else
    echo "tdnf update info not available yet!"
fi
