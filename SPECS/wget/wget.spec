Summary:        A network utility to retrieve files from the Web
Name:           wget
Version:        1.21.3
Release:        5%{?dist}
License:        GPLv3+
URL:            http://www.gnu.org/software/wget/wget.html
Group:          System Environment/NetworkingPrograms
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
%define sha512  %{name}=29889ecbf590dff0f39183d9e0621741d731a554d990e5c995a4644725dca62e8e19601d40db0ef7d62ebf54e5457c7409965e4832b6e60e4ccbc9c8caa30718
Patch0:         CVE-2024-38428.patch

Requires:       openssl
BuildRequires:  openssl-devel
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
