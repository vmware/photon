Summary:    A cloud-init implementation in C.
Name:       micro-config-drive
Version:    25
Release:    2%{?dist}
Group:      Development/Tools
License:    GPL-3.0
URL:        https://github.com/clearlinux/micro-config-drive
Source0:    https://github.com/clearlinux/micro-config-drive/releases/download/v%{version}/%{name}-%{version}.tar.xz
%define sha1 micro-config-drive=11945b6c13e5f5e126bc12906c69cc057026bc28
BuildRequires:    e2fsprogs-devel
BuildRequires:    shadow
BuildRequires:    check
BuildRequires:    glib-devel
BuildRequires:    json-glib-devel
BuildRequires:    curl
BuildRequires:    parted
BuildRequires:    libyaml-devel
BuildRequires:    systemd-devel
Requires:    json-glib
Requires:    glib
Requires:    libyaml
Requires:    parted

%description
A cloud-init for Clear Linux* Project for Intel Architecture.

%prep
%setup -q

%build
autoreconf -vif
%configure --disable-static --with-packagemgr=tdnf
make V=1 CFLAGS="%{optflags}" %{?_smp_mflags}

%check
make VERBOSE=1 V=1 %{?_smp_mflags} check

%install
rm -rf $RPM_BUILD_ROOT
%make_install

%post
%systemd_post ucd.service

%preun
%systemd_preun ucd.service

%postun
%systemd_postun_with_restart ucd.service


%files
%defattr(-,root,root,-)
%{_bindir}/ucd
/lib/systemd/system/ucd.service
/lib/systemd/system/multi-user.target.wants/ucd.service
%doc /usr/share/man/man1/*
%doc /usr/share/man/man5/*

%changelog
*    Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  25-2
-    Change systemd dependency
*    Wed Aug 3 2016 Divya Thaluru <dthaluru@vmware.com> 25-1
-    Initial version
