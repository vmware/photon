Summary:        The AWS SDK for Python
Name:           python3-boto3
Version:        1.24.56
Release:        2%{?dist}
License:        Apache 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/boto/boto3
Source0:        https://github.com/boto/boto3/archive/boto3-%{version}.tar.gz
%define sha512  boto3=7da4c3ba2bb3a75ef4e95ae5c6c90b6064f30064ee4db9a9b102b741a153372b460d86ad2e7098691ee9faf3fd9acd80dd6852e723b99278d8b26c42981333e1
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
Requires:       python3-botocore
Requires:       python3-s3transfer
BuildArch:      noarch
Provides:       python%{python3_version}dist(boto3)

%description
Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python,
which allows Python developers to write software that makes use of services like
Amazon S3 and Amazon EC2

%prep
%autosetup -n boto3-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.24.56-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.24.56-1
- Automatic Version Bump
* Wed Jul 21 2021 Tapas Kundu <tkundu@vmware.com> 1.16.13-2
- Added s3transfer to requires
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 1.16.13-1
- Automatic Version Bump
* Tue Sep 29 2020 Gerrit Photon <photon-checkins@vmware.com> 1.15.10-1
- Automatic Version Bump
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.15.5-1
- Automatic Version Bump
* Thu Sep 10 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.59-1
- Automatic Version Bump
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.58-1
- Automatic Version Bump
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.53-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.49-1
- Automatic Version Bump
* Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.41-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.28-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 1.9.0-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.9.0-1
- Update to version 1.9.0
* Wed Jan 24 2018 Kumar Kaushik <kaushikk@vmware.com> 1.5.9-1
- Initial packaging for photon.
