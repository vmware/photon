# Migrating Scripts to systemd

Although `systemd` maintains compatibility with `init.d` scripts, as a best practice, you must adapt the scripts that you want to run on Photon OS to `systemd` to avoid potential problems. 

Such a conversion standardizes the scripts, reduces the footprint of your code, makes the scripts easier to read and maintain, and improves their robustness on a `systemd` system.