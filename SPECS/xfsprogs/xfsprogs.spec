Summary:        Utilities for managing the XFS filesystem
Name:           xfsprogs
Version:        5.8.0
Release:        1%{?dist}
License:        GPL+ and LGPLv2+
URL:            http://oss.sgi.com/projects/xfs/
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://kernel.org/pub/linux/utils/fs/xfs/xfsprogs/%{name}-%{version}.tar.xz
%define sha1    xfsprogs=f0b8d80620e6ebd0b078a6123462d191d57a3ee2
BuildRequires:  gettext
BuildRequires:  readline-devel

%description
The xfsprogs package contains administration and debugging tools for the
XFS file system.

%package devel
Summary: XFS filesystem-specific static libraries and headers
Group: Development/Libraries
Requires: xfsprogs = %{version}-%{release}

%description devel
Libraries and header files needed to develop XFS filesystem-specific programs.

%package lang
Summary: Additional language files for xfsprogs
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of xfsprogs.

%prep
%setup -q

%build
%configure \
        --enable-readline=yes	\
	--enable-blkid=yes

make DEBUG=-DNDEBUG     \
     INSTALL_USER=root  \
     INSTALL_GROUP=root  %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} PKG_DOC_DIR=%{_usr}/share/doc/%{name}-%{version} install
make DESTDIR=%{buildroot} PKG_DOC_DIR=%{_usr}/share/doc/%{name}-%{version} install-dev

#find %{buildroot}/lib64/ -name '*.so' -delete
find %{buildroot}/%{_lib64dir} -name '*.la' -delete
find %{buildroot}/%{_lib64dir} -name '*.a' -delete

%find_lang %{name}

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}-%{version}/*
/sbin/*
/lib64/*.so.*.*
/usr/lib64/*/*.cron
%{_mandir}/man2/*
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_sbindir}/*
%exclude %{_docdir}/%{name}-%{version}/CHANGES.gz

%files devel
%defattr(-,root,root)
%dir %{_includedir}/xfs
%{_includedir}/xfs/*
/lib64/*.so
/lib64/*.so.1
%{_mandir}/man3/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*   Thu Sep 10 2020 Gerrit Photon <photon-checkins@vmware.com> 5.8.0-1
-   Automatic Version Bump
*   Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 5.7.0-1
-   Automatic Version Bump
*   Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 5.6.0-1
-   Automatic Version Bump
*   Tue Oct 22 2019 Prashant S Chauhan <psinghchauha@vmware.com> 4.18.0-2
-   Removed %check since this package does not come with test suite
*   Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 4.18.0-1
-   Updated to latest version
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 4.10.0-3
-   Use standard configure macros
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.10.0-2
-   Ensure non empty debuginfo
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 4.10.0-1
-   Updated to version 4.10.0.
*   Fri Jan 6 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.9.0-1
-   Initial build.  First version
