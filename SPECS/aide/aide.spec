Summary:        Intrusion detection environment
Name:           aide
Version:        0.17.4
Release:        7%{?dist}
URL:            https://github.com/aide/aide
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/aide/aide/releases/download/%{version}/%{name}-%{version}.tar.gz

Source1: %{name}.conf

Source2: license.txt
%include %{SOURCE2}

BuildRequires: build-essential
BuildRequires: pcre-devel
BuildRequires: libgpg-error-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: curl-devel
BuildRequires: libgcrypt-devel
BuildRequires: audit-devel
BuildRequires: libacl-devel
BuildRequires: attr-devel
BuildRequires: libselinux-devel
BuildRequires: e2fsprogs-devel

%if 0%{?with_check}
BuildRequires: check-devel
%endif

Requires: pcre
Requires: libgpg-error
Requires: openssl
Requires: libgcrypt
Requires: audit
Requires: libacl
Requires: attr
Requires: libselinux
Requires: curl-libs
Requires: e2fsprogs

%description
AIDE (Advanced Intrusion Detection Environment) is a file integrity
checker and intrusion detection program.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
export HAVE_CHECK=1
autoreconf -ivf
%configure  \
  --disable-static \
  --with-config_file=%{_sysconfdir}/%{name}.conf \
  --with-gcrypt \
  --with-zlib \
  --with-curl \
  --with-posix-acl \
  --with-selinux \
  --with-xattr \
  --with-e2fsattrs \
  --with-audit

%make_build

%install
%make_install %{?_smp_mflags}

mkdir -p %{buildroot}%{_sysconfdir} \
         %{buildroot}%{_sharedstatedir}/%{name} \
         %{buildroot}%{_var}/log/%{name} \

cp %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}.conf

chmod 600 %{buildroot}%{_sysconfdir}/%{name}.conf

chmod 700 %{buildroot}%{_sharedstatedir}/%{name} \
          %{buildroot}%{_var}/log/%{name}

%if 0%{?with_check}
%check
make check %{?_smp_mflags}
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_mandir}/*
%config(noreplace) %{_sysconfdir}/%{name}.conf
%dir %{_sharedstatedir}/%{name}
%{_var}/log/%{name}

%changelog
* Wed Mar 19 2025 Vamsi Krishna Brahmajosuyula <vamsi-krishna.brahmajosyula@vmware.com> 0.17.4-7
- Introduce license.txt
* Thu Aug 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.17.4-6
- Use database_in inplace of database in aide.conf
* Fri Apr 14 2023 Harinadh D <hdommaraju@vmware.com> 0.17.4-5
- version bump to use curl 8.0.1
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.17.4-4
- Bump version as a part of zlib upgrade
* Tue Mar 28 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 0.17.4-3
- In aide.conf removed verbose option and introduced log_level option
* Thu Dec 22 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 0.17.4-2
- Bump release as a part of libgpg-error upgrade to 1.46
* Thu Sep 15 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.17.4-1
- Upgrade to v0.17.4
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.16.2-2
- openssl 1.1.1
* Wed Aug 14 2019 Tapas Kundu <tkundu@vmware.com> 0.16.2-1
- Initial build for Photon
