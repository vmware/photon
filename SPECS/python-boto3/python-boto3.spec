%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Summary:        The AWS SDK for Python
Name:           python3-boto3
Version:        1.9.0
Release:        2%{?dist}
License:        Apache 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/boto/boto3
Source0:        https://github.com/boto/boto3/archive/boto3-%{version}.tar.gz
%define sha1    boto3=2c5174711d2a5c73a8dcc569734bbd94a9b63281
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
Requires:       python3-botocore
Requires:       python3-jmespath
Requires:       python3-dateutil
BuildArch:      noarch

%description
Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python,
which allows Python developers to write software that makes use of services like
Amazon S3 and Amazon EC2

%prep
%setup -q -n boto3-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 1.9.0-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.9.0-1
-   Update to version 1.9.0
*   Wed Jan 24 2018 Kumar Kaushik <kaushikk@vmware.com> 1.5.9-1
-   Initial packaging for photon.
