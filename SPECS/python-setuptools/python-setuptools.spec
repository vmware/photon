Summary: Download, build, install, upgrade, and uninstall Python packages
Name: python-setuptools
Version: 12.4
Release: 1%{?dist}
License: Python or ZPLv2.0
Group: Development/Languages
URL: https://pypi.python.org/pypi/setuptools

Source0: https://pypi.python.org/packages/source/s/setuptools/setuptools-%{version}.tar.gz
%define sha1 setuptools=427e916ad99a704af54b7aa3124bd52d4ebf04d3

BuildArch: noarch

BuildRequires: python2
BuildRequires: python2-libs

Requires: python2
Requires: python2-libs

%description
setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

%prep
%setup -n setuptools-%{version}

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build \
    --root "%{buildroot}" \
    --single-version-externally-managed
find %{buildroot}%{python_sitelib} -name '*.exe' | xargs rm -f
find %{buildroot}%{python_sitelib} -name '*.txt' | xargs chmod -x
chmod +x %{buildroot}%{python_sitelib}/setuptools/command/easy_install.py

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%doc *.txt
%{_bindir}/*
%{python_sitelib}/*

%changelog
* Wed Feb 11 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
