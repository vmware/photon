# Appendix

## Photon 1.0 GA: systemd-networkd and systemd-resolved not starting in the updated image, on reboot
This issue has been fixed in 1.0 Revision 2 and above.
If you compose a custom image at the server, download at the RPM-OSTree host the updated image and reboot, systemd-networkd may report an access denied error, in which case your network interface is not properly configured, and ifconfig will not list an external IP address. This is a bug that was discovered very late and we didn't have time to address it for Photon 1.0. The easy workaround is to temporary relax the server permissions before  composing the tree (image) and revert back to the secure umask after that. Here are the steps to recover, that work even after you've already composed a "bad" image and some hosts have downloaded and booted into it:  
At server:  
  1. Execute **umask 022**.  
  2. Execute **rpm-ostree compose tree --force-nocache ...** to create a new, good image.  
  3. Execute **umask 027** to tighten back the server permissions as good security practice.  

At every host that booted into the bad image, from console:  
  1. Execute **rpm-ostree rollback**, then reboot into the older good image.  
  2. Login after reboot, then execute **rpm-ostree upgrade** to download the new, good image from server. It's going to skip the bad image version.  
  3. Reboot into new good image and execute ifconfig, notice you now have an external IP address. Also, your host will have the recommended secure umask 0027 set.
 
## OSTree repo is no longer accessible via http after RPM-OSTree server has updated httpd package
If server itself is updated via tdnf that brings a newer version of httpd package, httpd.service file will be overwritten to a default value (not valid for OSTree repo), and hosts trying to install or upgrade will report an "invalid or missing config".  To fix the problem:  

* Replace the content of /usr/lib/systemd/system/httpd.service with:
```
[Unit]
Description=The Apache HTTP Server
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
ExecStart=/usr/sbin/httpd -f /srv/rpm-ostree/ostree-httpd.conf -DFORGROUND
ExecReload=/usr/sbin/httpd -f /srv/rpm-ostree/ostree-httpd.conf -k graceful
KillSignal=SIGWINCH
KillMode=mixed
Restart=always

[Install]
WantedBy=multi-user.target
```
* systemctl daemon-reload
* systemctl restart httpd

## Error composing when photon-iso repo is selected
If you are doing the trick explained in 9.3 to speed up composing by getting the RPMS from cdrom instead of the online repo, you may encounter an **error: cache too old:**. We are investigating - it could be an rpm-ostree bug or some incompatibility between the caching in tdnf vs. libhif used by ostree, but meanwhile just leave **"repos": ["photon"],** in photon-base.json.  
  
## Package differences between RPM-OSTree "minimal" and minimal installation profile
This is not an actual issue, I'm only mentioning because of naming - people may expect that installing an RPM-OSTree host using the **photon/1.0/x86_64/minimal** reftag will create an exact equivalent, albeit read-only replica of the Photon minimal, when in fact you get fewer packages. That is because we were constrained by size of the starter ostree repo included on the cdrom, needed in order to install fast the server and the default host, yet still small enough for the ISO installer to run in 384 MB RAM in Fusion and Workstation, 512 MB in ESX.

That's easy to overcome - just add the wanted package names in the photon-base.json and re-compose the tree.



## Manual pages not included for installed packages
The packages in photon-base.json don't have their manual pages installed. This is for the same reason - keep the cdrom included ostree repo size small. If the manual pages are desired, just change to true the **documentation** setting in photon-base.json and re-compose.


