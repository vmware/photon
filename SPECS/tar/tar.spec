Summary:    Archiving program
Name:       tar
Version:    1.34
Release:    3%{?dist}
License:    GPLv3+
URL:        http://www.gnu.org/software/tar
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://ftp.gnu.org/gnu/tar/%{name}-%{version}.tar.xz
%define sha512 %{name}=5e77c4a7b49983ad7d15238c2bce28be7a8aa437b4b1815fc00abd13096da308b6bba196cc6e3ed79d85e62823d520ae0d8fcda2d93873842cf84dc3369fc902

Patch0: CVE-2022-48303.patch

BuildRequires: libacl-devel

Requires: libacl

%description
Contains GNU archiving program

%prep
%autosetup -p1

%build
export FORCE_UNSAFE_CONFIGURE=1

%configure \
    --disable-silent-rules \
    --with-posix-acls

%make_build

%install
%make_install %{?_smp_mflags}

rm -rf %{buildroot}{%{_infodir},%{_mandir}}

%find_lang %{name}

%if 0%{?with_check}
%check
%make_build check
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/%{name}
%{_libexecdir}/rmt

%changelog
* Tue Jul 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.34-3
- Add acl support
- Fix CVE-2022-48303
* Wed Feb 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.34-2
- Fix binary path
* Thu Apr 08 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.34-1
- Update to version 1.34
* Mon Jul 13 2020 Gerrit Photon <photon-checkins@vmware.com> 1.32-1
- Automatic Version Bump
* Thu Mar 05 2020 Keerthana K <keerthanak@vmware.com> 1.30-3
- Fix CVE-2019-9923.
* Mon Mar 02 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.30-2
- Fix make check failure
* Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 1.30-1
- Update to version 1.30
* Tue Apr 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.29-1
- Update to version 1.29.
* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 1.28-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.28-2
- GA - Bump release of all rpms
* Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.28-1
- Update to 1.28-1.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.27.1-1
- Initial build. First version
