%define libedit_version 3.1
%define libedit_release 20210910

Summary:        The NetBSD Editline library
Name:           libedit
Version:        3.1.20210910
Release:        2%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        BSD
Url:            http://www.thrysoee.dk/editline/
Group:          Applications/Libraries

Source0:        libedit-%{libedit_release}-%{libedit_version}.tar.gz
%define sha512 %{name}=b7361c277f971ebe87e0e539e5e1fb01a4ca1bbab61e199eb97774d8b60dddeb9e35796faf9cc68eb86d1890e8aac11db13b44b57ccc8302d559741fbe9d979e

Requires:       ncurses

BuildRequires:  ncurses-devel

%description
Libedit is an autotool- and libtoolized port of the NetBSD
Editline library. It provides generic line editing, history, and
tokenization functions, similar to those found in GNU Readline.

%package        devel
Summary:        The NetBSD Editline library
Group:          Development/Libraries
Requires:       libedit = %{version}-%{release}

%description    devel
Development files for libedit

%prep
%autosetup -p1 -n libedit-%{libedit_release}-%{libedit_version}

%build
%configure --disable-static

%make_build %{?_smp_mflags}

%install
%make_install
find %{buildroot} -name '*.la' -delete
# Remove history.3, a solftlink to editline, which conflicts with readline-devel
rm -f %{buildroot}%{_mandir}/man3/history.3

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,0755)
%exclude %dir %{_libdir}/debug
%{_libdir}/*.so.*
%{_mandir}/*

%files devel
%defattr(-,root,root,0755)
%{_libdir}/*.so
%{_libdir}/pkgconfig
%{_includedir}/*

%changelog
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.1.20210910-2
- Exclude debug symbols properly
* Wed Dec 22 2021 Susant sahani <ssahani@vmware.com> 3.1.20210910-1
- Version bump
* Wed Sep 02 2020 Dweep Advani <dadvani@vmware.com> 3.1.20191231-2
- Fix conflict of /usr/share/man/man3/history.3 with readline-devel
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1.20191231-1
- Automatic Version Bump
* Tue Aug 14 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.20180525-1
- Initial
