%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Summary:        The AWS SDK for Python
Name:           python-boto3
Version:        1.5.9
Release:        1%{?dist}
License:        Apache 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/boto/boto3
Source0:        https://github.com/boto/boto3/archive/boto3-%{version}.tar.gz
%define         sha1 boto3=31713c7ba10901494321e2a11fe19fb86b0176d5
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs
Requires:       python-botocore
Requires:       python-jmespath
Requires:       python-dateutil
BuildArch:      noarch

%description
Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python, 
which allows Python developers to write software that makes use of services like 
Amazon S3 and Amazon EC2

%package -n     python3-boto3
Summary:        python3-boto3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs
Requires:       python3-botocore
Requires:       python3-jmespath
Requires:       python3-dateutil

%description -n python3-boto3
Python 3 version.

%prep
%setup -q -n boto3-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-boto3
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Fri Jan 05 2017 Kumar Kaushik <kaushikk@vmware.com> 1.5.9-1
-   Initial packaging for photon.
