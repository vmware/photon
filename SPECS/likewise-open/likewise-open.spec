Name:       likewise-open
Summary:    Likewise Open
Version:    6.2.11.13
Release:    8%{?dist}
Group:      Development/Libraries
Vendor:     VMware, Inc.
License:    GPL 2.0,LGPL 2.1
URL:        https://github.com/vmware/likewise-open
Distribution:   Photon
Source0:    %{name}-%{version}.tar.gz
%define sha512  %{name}=8531fb95f8d26c7356e1504ee1ffd8245fa1f84cb4d83151b690f20ec4aeec1e9f9a8eb0145d568688efcfba4433fbec9ee17af112409ab4ad4ceba4520d2ee3

Patch0:         likewise-open-openssl-1.1.1.patch
Patch1:         likewise-open-openssl-1.1.1-FixV2.patch
Patch2:         fix_arm_build_dcerpc_lwopen.patch
Patch3:         0001-likewise-open-compatibility-with-openssl-3.0.patch

Requires:       Linux-PAM
Requires:       (coreutils >= 8.22 or toybox)
Requires:       /bin/grep
Requires:       krb5 >= 1.12
Requires:       libxml2
Requires:       haveged >= 1.9
Requires:       openldap >= 2.4
Requires:       openssl >= 1.1.1
Requires:       (procps-ng or toybox)
Requires:       /bin/sed
Requires:       sqlite-libs

BuildRequires:  Linux-PAM-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  krb5-devel >= 1.12
BuildRequires:  libxml2-devel
BuildRequires:  openldap >= 2.4
BuildRequires:  openssl-devel >= 1.1.1
BuildRequires:  sqlite-devel

%define _likewise_prefix /opt/likewise
%define _likewise_bin %{_likewise_prefix}/bin
%define _likewise_sbin %{_likewise_prefix}/sbin

%package devel
Summary:        Likewise Open (development)
Group:          Development/Libraries
Requires:       likewise-open = %{version}-%{release}

%description
Likewise Open 6.1 LWIS

%description devel
This package provides files for developing against the Likewise APIs

%prep
%autosetup -p1

%build
# hack against glibc-2.26 to avoid getopt declaration mismatch
sed -i '/stdio.h/a#define _GETOPT_CORE_H 1' dcerpc/demos/echo_server/echo_server.c
pushd dcerpc
autoreconf -fi
popd
cd release
export CWD=$(pwd)

export LW_BUILD_PHOTON=1
export LW_FEATURE_LEVEL="auth"
export LSA_RPC_SERVERS="yes"
export LW_DEVICE_PROFILE="photon"

export CFLAGS="-Wno-error=unused-but-set-variable -Wno-error=implicit-function-declaration -Wno-error=sizeof-pointer-memaccess -Wno-error=unused-local-typedefs -Wno-error=pointer-sign -Wno-error=address -Wno-unused-but-set-variable -Wno-unused-const-variable -Wno-misleading-indentation -Wno-error=format-overflow -Wno-error=format-truncation -Wno-error=address-of-packed-member -Wno-error=nonnull -Wformat-overflow"
sh ../configure  --prefix=/opt/likewise \
             --libdir=/opt/likewise/lib64 \
             --datadir=/opt/likewise/share \
             --datarootdir=/opt/likewise/share \
             --build-isas=%{_arch} \
             --lw-bundled-libs='libedit' \
             --enable-vmdir-provider=yes \
             --disable-static \
             --at-build-string='%{_arch}-unknown-linux-gnu'
# fails with ${_smp_mflags}
make

%install
mkdir -p %{buildroot}
mv release/stage/* %{buildroot}
install -d %{buildroot}/var/lib/likewise/db
install -d %{buildroot}/var/lib/likewise/rpc
find %{buildroot} -name '*.in' -delete
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%pre
#
# Save pre-existing mech file for later concatentation to installed mech file
#
if [ -f /etc/gss/mech ]; then
  cp /etc/gss/mech /tmp/gss-mech-tmp
fi

case "$1" in
    1)
        #check if we are in chroot
        #If lwsmd service is running in vm, we still get the pidof lwsmd in chroot
        #and that causes us to exit with error.
        if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
            if [ -f /lib/systemd/system/lwsmd.service]; then
                echo "Likewise server Manager detected in chroot. Exiting."
                exit 1
            else
                echo "Likewise server Manager not detected in chroot."
                exit 0
            fi
        elif [ -n "`pidof lwsmd`" ]; then
            echo "Error: Likewise Service Manager detected. Exiting."
            exit 1
        fi
        ;;
esac

%post
#
# Merge saved off mech file with installed mech file
#
  if [ -f /tmp/gss-mech-tmp ]; then
    cat /etc/gss/mech >> /tmp/gss-mech-tmp
    grep '^[a-zA-Z0-9]' /tmp/gss-mech-tmp | sort -u > /etc/gss/mech
    rm -f /tmp/gss-mech-tmp
  fi

case "$1" in
    1)

    /bin/systemctl enable lwsmd.service >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        /bin/ln -s /lib/systemd/system/lwsmd.service /etc/systemd/system/multi-user.target.wants/lwsmd.service
    fi

    try_starting_lwregd_svc=true

    if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
        try_starting_lwregd_svc=false
    fi

    # handle installs when systemd might not be available (containers)
    /bin/systemctl >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        try_starting_lwregd_svc=false
    fi

    if [ $try_starting_lwregd_svc = true ]; then
        /bin/systemctl daemon-reload

        /bin/systemctl start lwsmd.service

        echo "Waiting for lwreg startup."
        while( test -z "`%{_likewise_prefix}/bin/lwsm status lwreg | grep standalone:`" )
        do
            echo -n "."
            sleep 1
        done
        echo "ok"
        for file in %{_likewise_prefix}/share/config/*.reg; do
            echo "Installing settings from $file..."
            %{_likewise_bin}/lwregshell import $file
        done
        %{_likewise_bin}/lwsm -q refresh
        sleep 2
        %{_likewise_bin}/lwsm start lsass
    else
        started_lwregd=false
        if [ -z "`pidof lwsmd`" ]; then
            %{_likewise_sbin}/lwregd &
            sleep 5
            started_lwregd=true
        fi
        for file in %{_likewise_prefix}/share/config/*.reg; do
            echo "Installing settings from $file..."
            %{_likewise_bin}/lwregshell import $file
        done
        if [ $started_lwregd = true ]; then
            kill -TERM `pidof lwregd`
            wait
        fi
    fi
    ;;

    2)
    ## Upgrade

    try_starting_lwregd_svc=true

    if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
        try_starting_lwregd_svc=false
    fi

    # handle upgrades when systemd might not be available (containers)
    /bin/systemctl >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        try_starting_lwregd_svc=false
    fi

    if [ $try_starting_lwregd_svc = true ]; then
        [ -z "`pidof lwsmd`" ] && /bin/systemctl start lwsmd.service

        echo "Waiting for lwreg startup."
        while( test -z "`%{_likewise_prefix}/bin/lwsm status lwreg | grep standalone:`" )
        do
            echo -n "."
            sleep 1
        done
        echo "ok"

        for file in %{_likewise_prefix}/share/config/*.reg; do
            echo "Upgrading settings from $file..."
            %{_likewise_bin}/lwregshell import $file
        done
        %{_likewise_bin}/lwsm -q refresh
        sleep 2
        %{_likewise_bin}/lwsm stop lwreg
        %{_likewise_bin}/lwsm start lsass
    else
        started_lwregd=false
        if [ -z "`pidof lwsmd`" ]; then
            %{_likewise_sbin}/lwregd &
            sleep 5
            started_lwregd=true
        fi
        for file in %{_likewise_prefix}/share/config/*.reg; do
            echo "Upgrading settings from $file..."
            %{_likewise_bin}/lwregshell import $file
        done
        if [ $started_lwregd = true ]; then
            kill -TERM `pidof lwregd`
            wait
        fi
    fi
    ;;

esac

%preun
#
# Save off a copy of gss/mech when it contains entries other than ntlm
#
if [ -f /etc/gss/mech ]; then
  if [ `grep -c -e '^[^n][^t][^l][^m]' /etc/gss/mech` -gt 0 ]; then
    cp /etc/gss/mech /tmp/gss-mech-tmp
  fi
fi

if [ "$1" = 0 ]; then
    %{_likewise_bin}/domainjoin-cli configure --disable pam
    %{_likewise_bin}/domainjoin-cli configure --disable nsswitch

    %{_likewise_bin}/lwsm stop lwreg

    /bin/systemctl stop lwsmd.service

    /bin/systemctl disable lwsmd.service

    if [ -f /etc/systemd/system/lwsmd.service ]; then
       /bin/rm -f /etc/systemd/system/lwsmd.service
    fi

fi

%postun
  #
  # Just remove the ntlm section added by Likewise.
  #
  if [ -f /tmp/gss-mech-tmp ]; then
    mkdir -p /etc/gss
    cat /tmp/gss-mech-tmp | sed '/^ntlm/d' > /etc/gss/mech
    #
    # Remove this file if it is empty; ntlm was the only mech entry.
    #
    if [ ! -s /etc/gss/mech ]; then
      rm -rf /etc/gss
    fi
    rm -f /tmp/gss-mech-tmp
  fi

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%exclude /etc/krb5.conf.default
/opt/likewise/bin/*
/opt/likewise/sbin/*
/opt/likewise/data/VERSION
/opt/likewise/share/config/*
/opt/likewise/lib64/*.so.*
/etc/gss/*
/lib/systemd/system/*
/etc/likewise/*
/lib64/libnss_lsass.so.*
/lib64/security/pam_lsass.so
/usr/lib64/gss/*.so
/opt/likewise/lib64/lwsm-loader/*.so
/opt/likewise/lib64/*.so
/opt/likewise/lib64/krb5/plugins/libkrb5/liblwnet_service_locator.so
%dir /var/lib/likewise
%dir /var/lib/likewise/db
%dir /var/lib/likewise/rpc

%files devel
%defattr(-,root,root)
/opt/likewise/include/*
/opt/likewise/lib64/pkgconfig/libedit.pc

%changelog
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 6.2.11.13-8
- Release bump up to use libxml2 2.9.12-1.
* Mon Jul 12 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 6.2.11.13-7
- openssl 3.0.0 compatibility
* Mon May 24 2021 Shreenidhi Shedi <sshedi@vmware.com> 6.2.11.13-6
- Fix aarch64 build errors
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 6.2.11.13-5
- GCC-10 support.
* Tue Nov 03 2020 Shreyas B. <shreyasb@vmware.com> 6.2.11.13-4
- Check NULL prior to use of HMAC_CTX_reset() & HMAC_CTX_free()
* Mon Aug 17 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 6.2.11.13-3
- Apply patches to use openssl-1.1.1
* Thu Apr 02 2020 Alexey Makhalov <amakhalov@vmware.com> 6.2.11.13-2
- Fix compilation issue with gcc-8.4.0
* Fri Aug 23 2019 Tapas Kundu <tkundu@vmware.com> 6.2.11.13-1
- Added checks to make sure if we are in chroot or not.
- Check pid of lwsmd when we are not in chroot.
* Wed Dec 12 2018 Sriram Nambakam <snambakam@vmware.com> 6.2.11.13-0
- Apply patches to source tar ball
* Mon Nov 5 2018 Sriram Nambakam <snambakam@vmware.com> 6.2.11.12-2
- Change domain join to recognize Photon release and use systemctl
* Mon Aug 13 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 6.2.11.12-1
- Update to version 6.2.11.12 and fix build issues with gcc 7.3
* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 6.2.11.4-4
- Aarch64 support
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 6.2.11.4-3
- Requires coreutils/procps-ng or toybox, /bin/grep, /bin/sed
* Thu Aug 24 2017 Alexey Makhalov <amakhalov@vmware.com> 6.2.11.4-2
- Fix compilation issue for glibc-2.26
* Wed Aug 09 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.2.11.4-1
- Update to 6.2.11.4.
* Wed Mar 29 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.2.11-1
- Initial - spec modified for Photon from likewise-open git repo.
