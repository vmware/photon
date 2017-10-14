Summary:    TCG Software Stack (TSS)
Name:       trousers
Version:    0.3.14
Release:    2%{?dist}
License:    BSD
URL:        https://sourceforge.net/projects/trousers/
Group:      System Environment/Security
Vendor:     VMware, Inc.
Distribution: Photon
Source0:    %{name}-%{version}.tar.gz
%define sha1 trousers=9ca2cc9e1179465f6c5d9055e2b855e25031b85a
Requires:   libtspi = %{version}-%{release}
%description
Trousers is an open-source TCG Software Stack (TSS), released under
the BSD License. Trousers aims to be compliant with the
1.1b and 1.2 TSS specifications available from the Trusted Computing

%package devel
Summary:    The libraries and header files needed for TSS development.
Requires:   libtspi = %{version}-%{release}
%description devel
The libraries and header files needed for TSS development.

%package -n libtspi
Summary:    TSPI library
%description -n libtspi
TSPI library

%prep
%setup -q -c %{name}-%{version}
%build
%configure \
    --disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%post
mkdir -p /var/lib/tpm
if [ $1 -eq 1 ]; then
    # this is initial installation
    if ! getent group tss >/dev/null; then
        groupadd tss
    fi
    if ! getent passwd tss >/dev/null; then
        useradd -c "TCG Software Stack" -d /var/lib/tpm -g tss \
            -s /bin/false tss
    fi
fi

%postun
if [ $1 -eq 0 ]; then
    # this is delete operation
    if getent passwd tss >/dev/null; then
        userdel tss
    fi
    if getent group tss >/dev/null; then
        groupdel tss
    fi
fi

%post -n libtspi -p /sbin/ldconfig
%postun	-n libtspi -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_sbindir}/*
%{_mandir}/man5
%{_mandir}/man8
%exclude /var

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libtspi.la
%{_libdir}/libtspi.so
%{_libdir}/libtspi.so.1
%{_mandir}/man3

%files -n libtspi
%defattr(-,root,root)
%{_libdir}/libtspi.so.1.2.0
%exclude %{_libdir}/debug
%exclude %{_libdir}/libtddl.a

%changelog
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.3.14-2
-   Use standard configure macros
*   Thu Mar 2 2017 Alexey Makhalov <amakhalov@vmware.com> 0.3.14-1
-   Initial build. First version
