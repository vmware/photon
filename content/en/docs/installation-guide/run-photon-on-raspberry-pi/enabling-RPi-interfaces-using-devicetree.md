---
title:  Enabling Raspberry Pi Interfaces using Device Tree
weight: 3
---

Photon OS RPI images from Photon 4.0 has Device Tree Overlay support. And these images have compiled Overlays to enable/disable Rpi Interface. Perform the following:

**SPI Interface**:
Execute following commands to enable SPI Interface:


    mkdir /sys/kernel/config/device-tree/overlays/

    cat /boot/efi/overlays/rpi-enable-spi0.dtbo > /sys/kernel/config/device-tree/overlays/spi/dtbo


**Audio Interface**:
Execute following commands to enable Audio Interface:

    mkdir  /sys/kernel/config/device-tree/overlays/audio

    cat /boot/efi/overlays/rpi-enable-audio.dtbo >  /sys/kernel/config/device-tree/overlays/audio/dtbo

**Note**: Ensure that the **linux-drivers-sound** rpm is installed.

**I2C Interface**:
Execute following command to enable I2C Interface:

```
modprobe i2c-dev
```

#Customizing Device Tree Overlay

Photon OS also provides Device Tree Compilers (i.e. dtc), to compile **Customised Device Tree Overlays**. Execute following command to install dtc on Photon OS:

```
tdnf install dtc
```
Execute following command to compile the overlay: 

```
dtc -@ -O dtb -o my_overlay_dt.dtbo my_overlay_dt.dts
```

For more information about format of Device Tree Overlay, see 
[https://www.kernel.org/doc/Documentation/devicetree/overlay-notes.txt](https://www.kernel.org/doc/Documentation/devicetree/overlay-notes.txt)


