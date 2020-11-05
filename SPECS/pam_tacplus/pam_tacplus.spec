Summary:        PAM Tacacs+ module
Name:           pam_tacplus
Version:        1.6.1
Release:        1%{?dist}
License:        GPL
URL:            http://tacplus.sourceforge.net/
Group:          System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        %{name}-%{version}.tar.gz
%define sha1    pam_tacplus=d39193bb09286492a33131aa193184484a6c1183

BuildRequires:  Linux-PAM-devel

%description
PAM Tacacs+ module based on code produced by Pawel Krawczyk <pawel.krawczyk@hush.com> and Jeroen Nijhof <jeroen@jeroennijhof.nl>

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

make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/etc/pam.d
mkdir -p %{buildroot}/%{_lib}/security

install -m 755 .libs/pam_tacplus.so %{buildroot}/%{_lib}/security/
install -m 644 sample.pam $RPM_BUILD_ROOT/etc/pam.d/tacacs

chmod 755 $RPM_BUILD_ROOT/%{_lib}/security/*.so*

make install DESTDIR=%{buildroot}
find %{buildroot}/usr/lib/ -name '*.la' -delete

%check
make %{?_smp_mflags} check

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
* Thu Nov 05 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.6.1-1
- Bump version to 1.6.1, fixes CVE-2020-27743
* Fri Aug 28 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.4.1-2
- Fixed CVE-2020-13881
* Tue Apr 11 2017 Xiaolin Li <xiaolinl@vmware.com> 1.4.1-1
- Initial packaging for Photon.
