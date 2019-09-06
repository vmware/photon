echo "Check for .config applicability"
make LC_ALL= olddefconfig
# Remove comment with a version string
sed -i '3d' .config
# Fail if any diffs
diff -u .config.old .config

