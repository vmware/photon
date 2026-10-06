echo "Check for .config applicability"
# make doesn't support _smp_mflags
make LC_ALL= olddefconfig
# Remove comment with a version string
sed -i '3d' .config
# Fail if any diffs
if [[ ! -f .config.old ]]; then
  echo "No change"
  exit 0
fi
diff -u .config.old .config

