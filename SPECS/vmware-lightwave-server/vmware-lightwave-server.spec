Name:          vmware-lightwave-server
Summary:       VMware Lightwave Server
Version:       1.2.0
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache 2.0
URL: 	       https://github.com/vmware/lightwave
Distribution:  Photon

Requires:  coreutils >= 8.22
Requires:  openssl >= 1.0.2
Requires:  likewise-open >= 6.2.11
Requires:  vmware-directory = %{version}
Requires:  vmware-afd = %{version}
Requires:  vmware-ca = %{version}
Requires:  vmware-ic-config = %{version}
Requires:  vmware-sts = %{version}
Requires:  vmware-dns = %{version}

%description
VMware Infrastructure Controller

%build

%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

%post

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade
case "$1" in
    1)
        # Configure syslog-ng
        LINE='@include "lightwave.conf.d"'
        FILE=/etc/syslog-ng/syslog-ng.conf
        if [ -f "$FILE" ]; then
            grep -qs "$LINE" "$FILE"
            if [ "$?" -ne 0 ]; then
                echo "$LINE" >> "$FILE"
                pid=$( pidof syslog-ng )
                if [ -n "$pid" ]; then
                    kill -HUP $pid
                fi
            fi
        fi
        ;;
esac

%preun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

%postun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

%files
%defattr(-,root,root,0755)

%changelog
*   Thu Mar 30 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.0-1
-   Initial - spec modified for Photon from lightwave git repo.
