Summary:        A network utility to retrieve files from the Web
Name:           wget
Version:        1.21.3
Release:        10%{?dist}
URL:            http://www.gnu.org/software/wget/wget.html
Group:          System Environment/NetworkingPrograms
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Patch0:         CVE-2024-38428.patch
Patch1:         CVE-2026-16599.patch
Patch2:         wget-CVE-2024-10524.patch
Patch3:         wget-CVE-2026-15146.patch
Patch4:         wget-CVE-2026-58469.patch
Patch5:         wget-CVE-2026-58470.patch
Patch6:         wget-CVE-2026-58471.patch
Patch7:         wget-CVE-2026-58472.patch
# Fix undefined behavior in is_valid_port(), introduced by the CVE-2024-10524 fix (Patch2)
Patch8:         wget-CVE-2024-10524-fix-is_valid_port.patch
# Fix maybe_prepend_scheme() incorrectly refusing URLs with a colon in the path, introduced by the CVE-2024-10524 fix (Patch2)
Patch9:         wget-CVE-2024-10524-fix-maybe_prepend_scheme.patch
# Fix inverted isspace check in clean_metalink_string(), a regression from the CVE-2026-58469 fix (Patch4)
Patch10:        wget-CVE-2026-58469-regression-fix.patch
# Fix buffer overflow in html_quote_string(), a regression from the CVE-2026-58472 fix (Patch7)
Patch11:        wget-CVE-2026-58472-regression-fix.patch

Requires:       openssl
BuildRequires:  openssl-devel
BuildRequires:  texinfo
%if 0%{?with_check}
BuildRequires:  perl
%endif

%description
The Wget package contains a utility useful for non-interactive
downloading of files from the Web.

%prep
%autosetup -p1

%build
%configure \
    --with-ssl=openssl \
    --disable-dependency-tracking \
    --disable-silent-rules

%make_build

%install
%make_install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_sysconfdir}

cat >> %{buildroot}%{_sysconfdir}/wgetrc <<-EOF
#   default root certs location
    ca_certificate=/etc/pki/tls/certs/ca-bundle.crt
EOF
rm -rf %{buildroot}/%{_infodir}
%find_lang %{name}
%find_lang %{name}-gnulib
%{_fixperms} %{buildroot}/*

%if 0%{?with_check}
%check
export PERL_MM_USE_DEFAULT=1
cpan HTTP::Daemon
make %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}/*

%files -f %{name}.lang -f %{name}-gnulib.lang
%defattr(-,root,root)
%config(noreplace) /etc/wgetrc
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Fri Sep 18 2026 Dweep Advani <dweep.advani@broadcom.com> 1.21.3-10
- Add upstream follow-up fixes for regressions/bugs introduced by
  Patch2 (CVE-2024-10524) and Patch4/Patch7 (CVE-2026-58469/CVE-2026-58472):
  is_valid_port() UB, maybe_prepend_scheme() path-colon bug,
  clean_metalink_string() inverted isspace check, and a buffer
  overflow in html_quote_string() left over by the CVE-2026-58472 fix
* Wed Sep 09 2026 Dweep Advani <dweep.advani@broadcom.com> 1.21.3-9
- Added texinfo to BuildRequires to fix error of makeinfo command not found
- Fix CVE-2024-10524, CVE-2026-15146, CVE-2026-58469, CVE-2026-58470, CVE-2026-58471 and CVE-2026-58472
* Mon Sep 07 2026 Mukul Sikka <mukul.sikka@broadcom.com> 1.21.3-8
- Patched for CVE-2026-16599
* Tue Jun 17 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.21.3-7
- Release bump for aarch64 SRP compliance
* Wed Dec 11 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 1.21.3-6
- Release bump for SRP compliance
* Tue Jul 23 2024 Oliver Kurth <oliver.kurth@broadcom.com> 1.21.3-5
- add patch to fix CVE-2024-38428
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.21.3-4
- Conflicting with toybox was a mishap, undo it.
* Fri Sep 16 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.21.3-3
- Added conflicts toybox >= 0.8.8
* Mon May 2 2022 Oliver Kurth <okurth@vmware.com> 1.21.3-2
- update to latest version
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.21.3-1
- Automatic Version Bump
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.20.3-3
- Bump up release for openssl
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.20.3-2
- openssl 1.1.1
* Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 1.20.3-1
- Automatic Version Bump
* Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 1.19.5-1
- Updated to latest version
* Tue Dec 19 2017 Xiaolin Li <xiaolinl@vmware.com> 1.19.1-4
- Fix CVE-2017-6508
* Mon Nov 20 2017 Xiaolin Li <xiaolinl@vmware.com> 1.19.1-3
- Fix CVE-2017-13089 and CVE-2017-13090
* Wed Aug 09 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.19.1-2
- Install HTTP::Daemon perl module for the tests to pass.
* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 1.19.1-1
- Updated to version 1.19.1.
* Tue Nov 29 2016 Anish Swaminathan <anishs@vmware.com>  1.18-1
- Upgrade wget versions - fixes CVE-2016-7098
* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 1.17.1-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.17.1-2
- GA - Bump release of all rpms
* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.17.1-1
- Upgrade version
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.15-1
- Initial build.  First version
