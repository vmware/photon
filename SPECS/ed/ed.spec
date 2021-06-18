Summary:        Ed - A line-oriented text editor
Name:           ed
Version:        1.16
Release:        2%{?dist}
URL:            https://www.gnu.org/software/ed/
License:        GPLv3
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://fossies.org/linux/privat/%{name}-%{version}.tar.gz
%define sha1    ed=0b3848694d96e399dd5234e16fb69e8cf95bf781
%description
Ed - A line-oriented text editor

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
*   Fri Jun 18 2021 Nitesh Kumar <kunitesh@vmware.com> 1.16-2
-   Removed devel Package
*   Wed Jul 15 2020 Gerrit Photon <photon-checkins@vmware.com> 1.16-1
-   Automatic Version Bump
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.14.2-2
-   Cross compilation support
*   Thu Sep 27 2018 Sujay G <gsujay@vmware.com> 1.14.2-1
-   Initial build.
