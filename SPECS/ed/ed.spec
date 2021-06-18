Summary:        Ed - A line-oriented text editor
Name:           ed
Version:        1.14.2
Release:        3%{?dist}
URL:            https://www.gnu.org/software/ed/
License:        GPLv3
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://fossies.org/linux/privat/%{name}-%{version}.tar.gz
%define sha1    ed=1e29267247d39338aa31f1839b8320b86f4c50ab
%description
Ed - A line-oriented text editor

%prep
%setup -q

%build
%configure
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
%{_mandir}/man1/*
%exclude %{_infodir}/dir

%changelog
*   Fri Jun 18 2021 Nitesh Kumar <kunitesh@vmware.com> 1.14.2-3
-   Removed devel Package
*   Tue Oct 27 2020 Dweep Advani <dadvani@vmware.com> 1.14.2-2
-   Removed /usr/share/info/dir from packaging
*   Thu Sep 27 2018 Sujay G <gsujay@vmware.com> 1.14.2-1
-   Initial build.
