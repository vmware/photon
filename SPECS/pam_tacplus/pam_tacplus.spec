Summary:        PAM Tacacs+ module
Name:           pam_tacplus
Version:        1.6.1
Release:        3%{?dist}
URL:            http://tacplus.sourceforge.net/
Group:          System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: %{name}-%{version}.tar.gz
%define sha512 %{name}=c994c21b2ce0febea4510ce6d301c80dcc20b10512bfaae634d82ec717b684d8de9d192e7b8f174eb9811ef405616dd63d095f640804fb2d5065d69b9cc7a3a4

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  Linux-PAM-devel

%description
PAM Tacacs+ module based on code produced by
Pawel Krawczyk <pawel.krawczyk@hush.com> and
Jeroen Nijhof <jeroen@jeroennijhof.nl>

%package devel
Summary:    Development files for pam_tacplus
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for pam_tacplus.

%prep
%autosetup -a 0 -p1

%build
autoreconf -i
%configure --disable-static

%make_build

%install
mkdir -p %{buildroot}%{_sysconfdir}/pam.d \
         %{buildroot}%{_lib}/security

install -m 755 .libs/pam_tacplus.so %{buildroot}%{_lib}/security/
install -m 644 sample.pam %{buildroot}%{_sysconfdir}/pam.d/tacacs

chmod 755 %{buildroot}%{_lib}/security/*.so*

%make_install %{?_smp_mflags}

%check
%make_build check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_lib}/security/*.so
%attr(0755,root,root) %{_lib}/*.so.*
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/tacacs
%doc AUTHORS COPYING README.md ChangeLog

%files devel
%defattr(-,root,root,-)
%attr(644,root,root) %{_includedir}/*
%attr(755,root,root) %{_lib}/*.so
%attr(644,root,root) %{_lib}/pkgconfig/*
%doc %{_docdir}/*

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.6.1-3
- Release bump for SRP compliance
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.6.1-2
- Bump up release for openssl
* Thu Nov 05 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.6.1-1
- Bump version to 1.6.1, fixes CVE-2020-27743
* Sat Aug 29 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.5.1-2
- Fixed CVE-2020-13881
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.1-1
- Automatic Version Bump
* Tue Apr 11 2017 Xiaolin Li <xiaolinl@vmware.com> 1.4.1-1
- Initial packaging for Photon.
