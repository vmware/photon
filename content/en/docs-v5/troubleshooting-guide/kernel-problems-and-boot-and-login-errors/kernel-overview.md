---
title:  Kernel Overview
weight: 1
---

You can use `dmesg` command to troubleshooting kernel errors. The `dmesg` command prints messages from the kernel ring buffer. 

The following command, for example, presents kernel messages in a human-readable format: 

	dmesg --human --kernel

To examine kernel messages as you perform actions, such as reproducing a problem, in another terminal, you can run the command with the `--follow` option, which waits for new messages and prints them as they occur: 

	dmesg --human --kernel --follow

The kernel buffer is limited in memory size. As a result, the kernel cyclically overwrites the end of the information in the buffer from which `dmesg` pulls information. The systemd journal, however, saves the information from the buffer to a log file so that you can access older information. 

To view it, run the following command: 

	journalctl -k

If required, you can check the modules that are loaded on your Photon OS machine by running the `lsmod` command. For example:  
```
lsmod
Module                  Size  Used by
xt_conntrack           16384  2
nft_compat             20480  2
nf_tables             204800  39 nft_compat
nfnetlink              20480  2 nft_compat,nf_tables
xt_LOG                 16384  0
nf_log_syslog          20480  0
nf_conntrack          114688  1 xt_conntrack
nf_defrag_ipv6         20480  1 nf_conntrack
nf_defrag_ipv4         16384  1 nf_conntrack
af_packet              45056  2
vmwgfx                294912  1
psmouse               110592  0
drm_ttm_helper         16384  1 vmwgfx
ttm                    53248  2 vmwgfx,drm_ttm_helper
vfat                   24576  1
drm_kms_helper        118784  1 vmwgfx
fat                    69632  1 vfat
syscopyarea            16384  1 drm_kms_helper
sysfillrect            16384  1 drm_kms_helper
sysimgblt              16384  1 drm_kms_helper
fb_sys_fops            16384  1 drm_kms_helper
evdev                  20480  2
mousedev               20480  0
button                 16384  0
sch_fq_codel           20480  2
drm                   368640  5 vmwgfx,drm_kms_helper,drm_ttm_helper,ttm
fuse                  114688  1
i2c_core               49152  2 drm_kms_helper,drm
dm_mod                131072  0
loop                   28672  0
backlight              16384  1 drm
configfs               36864  1
dmi_sysfs              16384  0
hid_generic            16384  0
usbhid                 28672  0
hid                   114688  2 usbhid,hid_generic
xhci_pci               16384  0
xhci_hcd              167936  1 xhci_pci
uhci_hcd               40960  0
ehci_pci               16384  0
crc32c_intel           24576  2
ehci_hcd               69632  1 ehci_pci
usbcore               217088  6 xhci_hcd,ehci_pci,usbhid,ehci_hcd,xhci_pci,uhci_hcd
sr_mod                 24576  0
cdrom                  49152  1 sr_mod
usb_common             16384  4 xhci_hcd,usbcore,ehci_hcd,uhci_hcd
rdrand_rng             16384  0
rng_core               20480  1 rdrand_rng
efivarfs               20480  1
ipv6                  450560  270
autofs4                36864  2
```
