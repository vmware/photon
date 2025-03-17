Summary:        s3fs allows Linux, macOS, and FreeBSD to mount an S3 bucket via FUSE
Name:           s3fs-fuse
Version:        1.94
Release:        2%{?dist}
Group:          Development/Tools
URL:            https://github.com/s3fs-fuse/s3fs-fuse
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/%{name}/%{name}/archive/refs/tags/%{name}-v%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.94-2
- Release bump for SRP compliance
* Thu Oct 03 2024 Tapas Kundu <tapas.kundu@broadom.com> 1.94-1
- Update to version 1.94
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.91-5
- Bump version as a part of openjdk11 upgrade
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.91-4
- Bump version as a part of libxml2 upgrade
* Thu Apr 13 2023 Harinadh D <hdommaraju@vmware.com> 1.91-3
- version bump to use curl 8.0.1
* Wed Sep 21 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 1.91-2
- Use openjdk11
* Thu Sep 08 2022 Sharan Turlapati <sturlapati@vmware.com> 1.91-1
- Initial version of s3fs-fuse for Photon
