%triggerin -- initramfs
mkdir -p %{_sharedstatedir}/rpm-state/initramfs/pending
touch %{_sharedstatedir}/rpm-state/initramfs/pending/%{uname_r}
echo "initrd generation of kernel %{uname_r} will be triggered later" >&2
