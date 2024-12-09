Summary:      Contains programs for manipulating text files
Name:         gawk
Version:      5.1.1
Release:      4%{?dist}
URL:          http://www.gnu.org/software/gawk
Group:        Applications/File
Vendor:       VMware, Inc.
Distribution: Photon

Source0: http://ftp.gnu.org/gnu/gawk/%{name}-%{version}.tar.xz
%define sha512 %{name}=794538fff03fdb9a8527a6898b26383d01988e8f8456f8d48131676387669a8bb3e706fa1a17f6b6316ddba0ebe653c24ad5dd769f357de509d6ec25f3ff1a43

Source1: license.txt
%include %{SOURCE1}

Provides:   /bin/awk
Provides:   /bin/gawk
Provides:   awk

BuildRequires: readline-devel

Requires:   mpfr
Requires:   gmp
Requires:   readline

%description
The Gawk package contains programs for manipulating text files.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules

%make_build

%install
%make_install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cp -v doc/{awkforai.txt,*.{eps,pdf,jpg}} %{buildroot}%{_defaultdocdir}/%{name}-%{version}
rm -rf %{buildroot}%{_infodir}
find %{buildroot}%{_libdir} -name '*.la' -delete

%find_lang %{name}

%if 0%{?with_check}
%check
sed -i 's/ pty1 / /' test/Makefile
make %{?_smp_mflags} check
%endif

%ldconfig_scriptlets

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/%{name}/*
%{_includedir}/*
%{_libexecdir}/*
%{_datarootdir}/awk/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*
%{_sysconfdir}/profile.d/gawk.csh
%{_sysconfdir}/profile.d/gawk.sh

%changelog
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.1.1-4
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.1.1-3
- Release bump for SRP compliance
* Wed Dec 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.1.1-2
- Bump version as a part of readline upgrade
* Thu Dec 02 2021 Susant Sahani <ssahani@vmware.com> 5.1.1-1
- Version Bump
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 5.1.0-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 5.0.1-1
- Automatic Version Bump
* Mon Sep 17 2018 Sujay G <gsujay@vmware.com> 4.2.1-1
- Bump version to 4.2.1
* Wed Apr 05 2017 Danut Moraru <dmoraru@vmware.com> 4.1.4-1
- Upgrade to version 4.1.4
* Wed Jan 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.1.3-4
- Bump up for depending on readline 7.0
* Sun Dec 18 2016 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-3
- Provides /bin/awk
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.1.3-2
- GA - Bump release of all rpms
* Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 4.1.3-1
- Updated to version 4.1.3
* Fri Jun 19 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.0-2
- Provide /bin/gawk.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.1.0-1
- Initial build. First version
