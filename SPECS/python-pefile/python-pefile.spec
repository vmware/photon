%define debug_package %{nil}
%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        pefile, Portable Executable reader module
Name:           python-pefile
Version:        2019.4.18
Release:        1%{?dist}
Url:            https://pypi.org/project/pefile
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/36/58/acf7f35859d541985f0a6ea3c34baaefbfaee23642cf11e85fe36453ae77/pefile-%{version}.tar.gz
%define sha1    pefile=4cadf66db1e8640733054f7b2e1920900dfed704
BuildRequires:  python2
BuildRequires:  python-setuptools

BuildRequires:  python3
BuildRequires:  python3-setuptools

Requires:       python2
Requires:       python-future

%description
pefile, Portable Executable reader module
Processed elements such as the import table are made available with lowercase names,
to differentiate them from the upper case basic structure names.

%package -n     python3-pefile
Summary:        python3-pefile
Requires:       python3
Requires:       python3-future

%description -n python3-pefile
Python 3 version.

%prep
%setup -q -n pefile-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --skip-build --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-pefile
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Thu Feb 11 2021 Ankit Jain <ankitja@vmware.com> 2019.4.18-1
-   Initial packaging
