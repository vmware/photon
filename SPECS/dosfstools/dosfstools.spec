Summary:        Dos Filesystem tools
Name:           dosfstools
Version:        4.2
Release:        2%{?dist}
URL:            http://github.com/dosfstools/dosfstools
Group:          Filesystem Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

%description
dosfstools contains utilities for making and checking MS-DOS FAT filesystems.

%prep
%autosetup -p1

%build
./autogen.sh
%configure --enable-compat-symlinks
make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} PREFIX="/usr" install %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/man8/*
%{_docdir}/dosfstools/*

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 4.2-2
- Release bump for SRP compliance
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 4.2-1
- Automatic Version Bump
* Thu May 04 2017 Chang Lee <changlee@vmware.com> 4.1-2
- Add .vfat and .msdos symlinks back.
* Fri Mar 31 2017 Chang Lee <changlee@vmware.com> 4.1-1
- Updated package version
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.26-2
- GA - Bump release of all rpms
* Tue Jul 01 2014 Sharath George <sharathg@vmware.com> 3.0.26-1
- Initial build. First version
