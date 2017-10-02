# FIXME: noarch or generate debuginfo
%define debug_package %{nil}

%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python Build Reasonableness
Name:           python-pbr
Version:        2.1.0
Release:        1%{?dist}
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://docs.openstack.org/developer/pbr/
Source0:        https://pypi.io/packages/source/p/pbr/pbr-%{version}.tar.gz
%define sha1	pbr=cb5278676a96b429e491435ac04cfaf97b41d1c5

BuildRequires:  python-docutils
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
Requires:       python2
%description
A library for managing setuptools packaging needs in a consistent manner.

%package -n     python3-pbr
Summary:        Python Build Reasonableness
BuildRequires:  python3-devel
Requires:       python3

%description -n python3-pbr
Python 3 version.

%prep
%setup -q -n pbr-%{version}
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
%license LICENSE
%doc README.rst
%{_bindir}/pbr
%{python2_sitelib}/pbr-%{version}-*.egg-info
%{python2_sitelib}/pbr

%files -n python3-pbr
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{python3_sitelib}/pbr-%{version}-*.egg-info
%{python3_sitelib}/pbr

%changelog
*   Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.1.0-1
-   Initial packaging for Photon
