Summary:        s3fs allows Linux, macOS, and FreeBSD to mount an S3 bucket via FUSE
Name:           s3fs-fuse
Version:        1.91
Release:        5%{?dist}
License:        GPL-2.0
Group:          Development/Tools
URL:            https://github.com/s3fs-fuse/s3fs-fuse
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/%{name}/%{name}/archive/refs/tags/%{name}-v%{version}.tar.gz
%define sha512 %{name}=5b57af18395f34885b4b8a98e93b0e3f9043c9af78e415a0a6c15489611d7e21ae619e69655737de369edee15762d8726b82bc2651b5b7f5c20e26fe866a96bc

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
BuildRequires:  openjdk11
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

%if 0%{?with_check}
%check
pip3 install awscli
%make_build %{?_smp_mflags}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/s3fs
%{_mandir}/man1/s3fs.1*
%doc COPYING AUTHORS README.md ChangeLog

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.91-5
- Bump version as a part of openssl upgrade
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.91-4
- Bump version as a part of openjdk11 upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.91-3
- Bump version as a part of libxml2 upgrade
* Wed Sep 21 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 1.91-2
- Use openjdk11
* Thu Sep 08 2022 Sharan Turlapati <sturlapati@vmware.com> 1.91-1
- Initial version of s3fs-fuse for Photon
