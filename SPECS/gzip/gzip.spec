Summary:    Programs for compressing and decompressing files
Name:       gzip
Version:    1.12
Release:    4%{?dist}
URL:        http://www.gnu.org/software
Group:      Applications/File
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    http://ftp.gnu.org/gnu/gzip/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  less

%description
The Gzip package contains programs for compressing and
decompressing files.

%prep
%autosetup -p1

%build
#make some fixes required by glibc-2.28:
sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h

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
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.12-4
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.12-3
- Release bump for SRP compliance
* Wed May 18 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.12-2
- Add less to BuildRequires, required to build zless binary
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.12-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.10-1
- Automatic Version Bump
* Thu Aug 22 2019 Prashant Singh Chauhan <psinghchauha@vmware.com> 1.9-2
- Fix for make check failure
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 1.9-1
- Update to version 1.9
* Sat Sep 08 2018 Alexey Makhalov <amakhalov@vmware.com> 1.8-2
- Fix compilation issue against glibc-2.28
* Fri Mar 24 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.8-1
- Upgrading to version 1.8
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6-2
- GA - Bump release of all rpms
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.6-1
- Initial build. First version.
