%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Summary:        Amazon Web Services Library.
Name:           python-botocore
Version:        1.8.15
Release:        1%{?dist}
License:        Apache 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/boto/botocore
Source0:        https://github.com/boto/botocore/archive/botocore-%{version}.tar.gz
%define         sha1 botocore=6ecad01c8235e53d22da5e2da65704cede758550
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs
BuildArch:      noarch

%description
A low-level interface to a growing number of Amazon Web Services. The botocore package is the foundation for the AWS CLI as well as boto3.

%package -n     python3-botocore
Summary:        python3-botocore
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs

%description -n python3-botocore
Python 3 version.

%prep
%setup -q -n botocore-%{version}
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

%files -n python3-botocore
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Mon Dec 18 2017 Kumar Kaushik <kaushikk@vmware.com> 1.8.15-1
-   Initial packaging for photon.
