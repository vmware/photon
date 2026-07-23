%global build_if %{photon_subrelease} == 91

Summary:      Contains programs for manipulating text files
Name:         gawk
Version:      5.3.2
Release:      4%{?dist}
URL:          http://www.gnu.org/software/gawk
Group:        Applications/File
Vendor:       VMware, Inc.
Distribution: Photon

Source0: http://ftp.gnu.org/gnu/gawk/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

Provides:   /bin/awk
Provides:   /bin/gawk
Provides:   awk

BuildRequires: readline-devel

Obsoletes:  %{name}-extras
Conflicts:  %{name}-extras < 5.3.2-3

Requires:   %{name}-bin = %{version}-%{release}

%description
The Gawk package contains programs for manipulating text files.

%package bin
Summary:  Gawk binary
Conflicts: %{name} < 5.3.2-2
Requires:   mpfr
Requires:   gmp
Requires:   readline

%description bin
%{summary}

%package all-langpacks
Summary:    Additional localisation files for gawk utility
Conflicts:  %{name} < 5.3.2-1

%description all-langpacks
The base package of gawk supports only the english localisation.
This subpackage contains additional localisation files.

%package devel
Summary:    Header file for gawk extensions development
Requires:   %{name} = %{version}-%{release}
Conflicts:  %{name} < 5.3.2-1

%description devel
This subpackage provides /usr/include/gawkapi.h header file, which contains
definitions for use by extension functions calling into gawk. For more info
about gawk extensions, please refer to `The GNU Awk User's Guide`.

However, unless you are developing an extension to gawk, you most likely do not
need this subpackage.

%package doc
Summary:    Documentation files for gawk
BuildArch:  noarch
Requires:   %{name} = %{version}-%{release}
Conflicts:  %{name} < 5.3.2-1

%description doc
%{summary}

%prep
%autosetup -p1

%build
%configure --disable-silent-rules

%make_build

%install
%make_install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_docdir}/%{name}-%{version}
cp -av doc/{awkforai.txt,*.{eps,pdf,jpg}} %{buildroot}%{_docdir}/%{name}-%{version}
rm -r %{buildroot}%{_infodir}
find %{buildroot}%{_libdir} -name '*.la' -delete

%find_lang %{name}

%if 0%{?with_check}
%check
sed -i 's/ pty1 / /' test/Makefile
%make_build check
%endif

%files
%defattr(-,root,root)
%{_libdir}/*awk
%{_libexecdir}/*awk
%{_sysconfdir}/profile.d/gawk.*
%{_bindir}/gawkbug
%{_datadir}/*awk

%files bin
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/awk
%{_bindir}/%{name}-%{version}

%files devel
%defattr(-,root,root,-)
%{_includedir}/gawkapi.h

%files -f %{name}.lang all-langpacks
%defattr(-,root,root,-)

%files doc
%defattr(-,root,root,-)
%{_mandir}/*/*
%{_docdir}/%{name}-%{version}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.3.2-4
- Extended to build for subrelease 91 and above
* Fri Mar 06 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.3.2-3
- Remove extras sub package, unnecessary
* Mon Mar 02 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.3.2-2
- Introduce bin subpackage
* Mon Feb 09 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.3.2-1
- Split package into further sub packages
- Upgrade to v5.3.2
* Wed Jul 30 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 5.1.1-6
- Remove unintended license for SRP compliance
* Tue Jun 17 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.1.1-5
- Release bump for aarch64 SRP compliance
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
