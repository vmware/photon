Summary:    Stream editor
Name:       sed
Version:    4.8
Release:    5%{?dist}
URL:        http://www.gnu.org/software/sed
Group:      Applications/Editors
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    http://ftp.gnu.org/gnu/sed/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libacl-devel

Requires:       libacl

Conflicts:      toybox < 0.8.2-2

Provides:       /bin/sed

%description
The Sed package contains a stream editor.

%package lang
Summary:    Additional language files for sed
Group:      System Environment/Programming
Requires:   sed >= 4.5

%description lang
These are the additional language files of sed.

%prep
%autosetup -p1

%build
%configure \
    --htmldir=%{_defaultdocdir}/%{name}-%{version} \
    --disable-silent-rules

%make_build

%install
%make_install %{?_smp_mflags}
rm -rf %{buildroot}%{_infodir}

%find_lang %{name}

%if 0%{?with_check}
%check
sed -i 's|print_ver_ sed|Exit $fail|g' testsuite/panic-tests.sh
sed -i 's|compare exp-out out|#compare exp-out out|g' testsuite/subst-mb-incomplete.sh
make check %{?_smp_mflags}
%endif

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 4.8-5
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.8-4
- Release bump for SRP compliance
* Wed Nov 08 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.8-3
- Add libacl-devel to BuildRequires for ACL support
* Wed Feb 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.8-2
- Fix binary path
* Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 4.8-1
- Automatic Version Bump
* Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 4.5-2
- Do not conflict with toybox >= 0.8.2-2
* Tue Sep 18 2018 Srinidhi Rao <srinidhir@vmware.com> 4.5-1
- Updating to version 4.5
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4-3
- Added conflicts toybox
* Tue Aug 01 2017 Chang Lee <changlee@vmware.com> 4.4-2
- Skip panic-tests and subst-mb-incomplete from %check
* Thu Apr 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.4-1
- Update to version 4.4
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 4.2.2-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.2-2
- GA - Bump release of all rpms
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.2.2-1
- Initial build. First version
