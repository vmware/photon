%define libedit_version 3.1
%define libedit_release 20210910

Summary:        The NetBSD Editline library
Name:           libedit
Version:        3.1.20210910
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        libedit-%{libedit_release}-%{libedit_version}.tar.gz
%define sha1    libedit=855747cff17110fb59703b5b957d11c8f76b91ef
License:        BSD
Url:            http://www.thrysoee.dk/editline/
Group:          Applications/Libraries
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
%autosetup -n libedit-%{libedit_release}-%{libedit_version}

%build
%configure \
--disable-static
%make_build %{?_smp_mflags}

%install
%make_install
find %{buildroot} -name '*.la' -delete
# Remove history.3, a solftlink to editline, which conflicts with readline-devel
rm -f %{buildroot}/%{_mandir}/man3/history.3

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,0755)
%exclude %{_libdir}/debug
%{_libdir}/*.so.*
%{_mandir}/*

%files devel
%defattr(-,root,root,0755)
%{_libdir}/*.so
%{_libdir}/pkgconfig
%{_includedir}/*

%changelog
* Wed Dec 22 2021 Susant sahani <ssahani@vmware.com> 3.1.20210910-1
- Version bump
* Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 3.1.20210419-1
- Automatic Version Bump
* Wed Apr 14 2021 Gerrit Photon <photon-checkins@vmware.com> 3.1.20210419-1
- Automatic Version Bump
* Wed Sep 02 2020 Dweep Advani <dadvani@vmware.com> 3.1.20191231-2
- Fix conflict of /usr/share/man/man3/history.3 with readline-devel
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1.20191231-1
- Automatic Version Bump
* Tue Aug 14 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.20180525-1
- Initial
