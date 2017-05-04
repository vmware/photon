%triggerin -- initramfs
mkdir -p %{_localstatedir}/lib/rpm-state/initramfs/kernel.pending
touch %{_localstatedir}/lib/rpm-state/initramfs/kernel.pending/%{uname_r}
echo "initrd generation of kernel %{uname_r} will be triggered later" >&2
if [ $2 -eq 1 ]; then
  sed -i 's/^#photon_initrd=initrd.img-%{uname_r}$/photon_initrd=initrd.img-%{uname_r}/g' /boot/linux-%{uname_r}.cfg || :
fi

%triggerun -- initramfs
rm -rf %{_localstatedir}/lib/rpm-state/initramfs/kernel.pending/%{uname_r}
rm -rf /boot/initrd.img-%{uname_r}
echo "initrd of kernel %{uname_r} removed" >&2
if [ $2 -eq 0 ]; then
  sed -i 's/^photon_initrd=initrd.img-%{uname_r}$/#photon_initrd=initrd.img-%{uname_r}/g' /boot/linux-%{uname_r}.cfg || :
fi
