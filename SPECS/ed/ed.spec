Summary:        Ed - A line-oriented text editor
Name:           ed
Version:        1.14.2
Release:        2%{?dist}
URL:            https://www.gnu.org/software/ed/
License:        GPLv3
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://fossies.org/linux/privat/%{name}-%{version}.tar.gz
%define sha1    ed=1e29267247d39338aa31f1839b8320b86f4c50ab
%description
Ed - A line-oriented text editor
%package    devel
Summary:    Header and development files for ed
Requires:   %{name} = %{version}
%description    devel
GNU ed is a line-oriented text editor. It is used to create, display, modify and otherwise manipulate text files, both interactively and via shell scripts.
%prep
%setup -q
%build
sh configure --prefix=/usr CC=%{_host}-gcc
make V=1 %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}%{_lib}

%check
make  %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/ed
%{_bindir}/red
%{_infodir}/*
%exclude %{_datadir}/info/dir
%{_mandir}/man1/*

%changelog
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.14.2-2
-   Cross compilation support
*   Thu Sep 27 2018 Sujay G <gsujay@vmware.com> 1.14.2-1
-   Initial build.
