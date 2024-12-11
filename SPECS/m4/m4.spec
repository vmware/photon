Summary:       A macro processor
Name:          m4
Version:       1.4.19
Release:       3%{?dist}
URL:           http://www.gnu.org/software/m4
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon

Source0:       http://ftp.gnu.org/gnu/m4/%{name}-%{version}.tar.gz
%define sha512 m4=f5dd0f02fcae65a176a16af9a8e1747c26e9440c6c224003ba458d3298b777a75ffb189aee9051fb0c4840b2a48278be4a51d959381af0b1d627570f478c58f2

Source1: license.txt
%include %{SOURCE1}

%description
The M4 package contains a macro processor

%prep
%autosetup

%build
#make some fixes required by glibc-2.28:
sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h

%configure \
    --disable-silent-rules

%make_build

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
sed -i -e '41s/ENOENT/& || errno == EINVAL/' tests/test-readlink.h
make  %{?_smp_mflags}  check

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.4.19-3
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.4.19-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.4.19-1
- Fix compilation issue against glibc-2.36
* Fri Nov 09 2018 Alexey Makhalov <amakhalov@vmware.com> 1.4.18-3
- Cross compilation support
* Sun Sep 09 2018 Alexey Makhalov <amakhalov@vmware.com> 1.4.18-2
- Fix compilation issue against glibc-2.28
* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 1.4.18-1
- Update package version
* Fri Oct 07 2016 ChangLee <changlee@vmware.com> 1.4.17-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.4.17-2
- GA - Bump release of all rpms
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.4.17-1
- Initial build. First version
