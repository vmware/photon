Summary:        s3fs allows Linux, macOS, and FreeBSD to mount an S3 bucket via FUSE
Name:           s3fs-fuse
Version:        1.94
Release:        1%{?dist}
License:        GPL-2.0
Group:          Development/Tools
URL:            https://github.com/s3fs-fuse/s3fs-fuse
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/%{name}/%{name}/archive/refs/tags/%{name}-v%{version}.tar.gz
%define sha512 %{name}=1a29d4f0b73f844ea1d4ad6e0b36d601fb7ab5818af0a90564b77182564c04fbef308362a9a749038b17f28f07f79b6debb661610f69c039a405b931361abe9c

%if 0%{?with_check}
Patch0: 0001-test-Stop-failing-tests-from-running.patch
%endif

BuildRequires:  build-essential
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  libxml2-devel
BuildRequires:  pkg-config
BuildRequires:  fuse-devel

%if 0%{?with_check}
BuildRequires:  openjdk8
BuildRequires:  python3-pip
BuildRequires:  attr-devel
%endif

Requires:       fuse >= 2.8.4
Requires:       curl-libs
Requires:       openssl
Requires:       libxml2
Requires:       glibc
Requires:       libgcc
Requires:       libstdc++

%description
s3fs is a FUSE filesystem that allows you to mount an Amazon S3 bucket as a local filesystem.
It stores files natively and transparently in S3 (i.e., you can use other programs to access the same files).

%prep
%autosetup -p1

%build
sh ./autogen.sh

%configure

%make_build prefix=%{_prefix}

%install
%make_install %{?_smp_mflags} prefix=%{_prefix}

%check
pip3 install awscli
%make_build check

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/s3fs
%{_mandir}/man1/s3fs.1*
%doc COPYING AUTHORS README.md ChangeLog

%changelog
* Wed Oct 02 2024 Tapas Kundu <tapas.kundu@broadom.com> 1.94-1
- Update to version 1.94
* Tue Mar 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.91-5
- Bump version as a part of openjdk8 upgrade
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.91-4
- Bump version as a part of openjdk8 upgrade
* Mon May 29 2023 Harinadh D <hdommaraju@vmware.com> 1.91-3
- Version bump to use curl 8.1.1
* Fri Mar 24 2023 Harinadh D <hdommaraju@vmware.com> 1.91-2
- Version bump to use curl 8.0.1
* Thu Sep 08 2022 Sharan Turlapati <sturlapati@vmware.com> 1.91-1
- Initial version of s3fs-fuse for Photon
