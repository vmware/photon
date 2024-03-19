Summary:        s3fs allows Linux, macOS, and FreeBSD to mount an S3 bucket via FUSE
Name:           s3fs-fuse
Version:        1.91
Release:        4%{?dist}
License:        GPL-2.0
Group:          Development/Tools
URL:            https://github.com/s3fs-fuse/s3fs-fuse
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/%{name}/%{name}/archive/refs/tags/%{name}-v%{version}.tar.gz
%define sha512  s3fs-fuse=5b57af18395f34885b4b8a98e93b0e3f9043c9af78e415a0a6c15489611d7e21ae619e69655737de369edee15762d8726b82bc2651b5b7f5c20e26fe866a96bc
%if 0%{?with_check}
Patch0:         0001-test-Stop-failing-tests-from-running.patch
%endif

BuildRequires:  build-essential
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  libxml2-devel
BuildRequires:  pkg-config
BuildRequires:  fuse-devel >= 2.8.4
%if 0%{?with_check}
BuildRequires:  openjdk8
BuildRequires:  python3-pip
BuildRequires:  attr
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
%autosetup -p1 -n %{name}-%{version}

%build
./autogen.sh
%configure
%make_build prefix=%{_prefix}

%install
%make_install %{?_smp_mflags} prefix=%{_prefix}

%check
pip3 install awscli
make check %{?_smp_mflags}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/s3fs
%{_mandir}/man1/s3fs.1*
%doc COPYING AUTHORS README.md ChangeLog

%changelog
* Tue Mar 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.91-4
- Bump version as a part of openjdk8 upgrade
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.91-3
- Bump version as a part of openjdk8 upgrade
* Mon May 29 2023 Harinadh D <hdommaraju@vmware.com> 1.91-2
- Version bump to use curl 8.1.1
* Thu Sep 08 2022 Sharan Turlapati <sturlapati@vmware.com> 1.91-1
- Initial version of s3fs-fuse for Photon
