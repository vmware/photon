Summary:    Programs for compressing and decompressing files
Name:       gzip
Version:    1.12
Release:    2%{?dist}
License:    GPLv3+
URL:        http://www.gnu.org/software
Group:      Applications/File
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    http://ftp.gnu.org/gnu/gzip/%{name}-%{version}.tar.xz
%define sha1 %{name}=318107297587818c8f1e1fbb55962f4b2897bc0b

BuildRequires:  less

%description
The Gzip package contains programs for compressing and
decompressing files.

%prep
%setup -q

%build
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_bindir}
rm -rf %{buildroot}%{_infodir}

%check
%if 0%{?with_check}
make %{?_smp_mflags} check
%endif

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Wed May 18 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.12-2
- Add less to BuildRequires, required to build zless binary
* Thu Apr 07 2022 Siju Maliakkal <smaliakkal@vmware.com> 1.12-1
- Upgrade to l.12 to mitigate CVE-2022-1271
* Fri Mar 24 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.8-1
- Upgrading to version 1.8
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6-2
- GA - Bump release of all rpms
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.6-1
- Initial build.  First version
