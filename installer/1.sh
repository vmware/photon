#! /bin/bash
./mk-efiboot-img.sh
mkisofs -R -l -L -D -b isolinux/isolinux.bin -c isolinux/boot.cat \
		-no-emul-boot -boot-load-size 4 -boot-info-table \
		-eltorito-alt-boot -e efi/boot/efiboot.img -no-emul-boot \
		-V "PHOTON_$(date +%Y%m%d)" \
		./BUILD_DVD/ > 1.iso
