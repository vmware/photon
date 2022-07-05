Summary:        The GNU Database Manager
Name:           gdbm
Version:        1.22
Release:        1%{?dist}
License:        GPLv3+
URL:            http://www.gnu.org/software/gdbm
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://ftp.gnu.org/gnu/gdbm/%{name}-%{version}.tar.gz
%define sha1    gdbm=c45cc0178cbf41828369b07749d41778741703bd

%description
This is a disk file format database which stores key/data-pairs in
single files. The actual data of any record being stored is indexed
by a unique key, which can be retrieved in less time than if it was
stored in a text file.

%package lang
Summary:        Additional language files for gdbm
Group:          Applications/Databases
Requires:       %{name} = %{version}-%{release}
%description lang
These are the additional language files of gdbm

%package        devel
Summary:        Header and development files for gdbm
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications.

%prep
%autosetup -p1

%build
%configure \
    --enable-libgdbm-compat \
    --disable-silent-rules
%make_build %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}

find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
make %{?_smp_mflags} check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Thu Dec 02 2021 Susant Sahani <ssahani@vmware.com> 1.22-1
- Version Bump
* Thu Feb 11 2021 Tapas Kundu <tkundu@vmware.com> 1.19-1
- Update to 1.19
* Tue Jan 12 2021 Alexey Makhalov <amakhalov@vmware.com> 1.18.1-2
- GCC-10 support
* Mon Aug 24 2020 Keerthana K <keerthanak@vmware.com> 1.18.1-1
- Update to version 1.18.1
* Fri Nov 09 2018 Alexey Makhalov <amakhalov@vmware.com> 1.18-2
- Cross compilation support
* Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 1.18-1
- Update to version 1.18
* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 1.13-3
- Add devel package.
* Tue May 02 2017 Anish Swaminathan <anishs@vmware.com> 1.13-2
- Add lang package.
* Wed Apr 05 2017 Danut Moraru <dmoraru@vmware.com> 1.13-1
- Upgrade gdbm to 1.13
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.11-2
- GA - Bump release of all rpms
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.11-1
- Initial build. First version
