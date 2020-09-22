Summary:        Easily build and distribute Python packages
Name:           python3-setuptools
Version:        50.3.0
Release:        1%{?dist}
License:        PSF
URL:            http://www.python.org/
Group:          System Environment/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/pypi/%{srcname}/%{name}-%{version}.zip
%define sha1    python3-setuptools=d2cb560be03cf3aa3f7bfa96137dfd56f1f4c591

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  unzip

Requires:       python3
Requires:       python3-xml

Provides:       python3dist(setuptools) = %{version}
Provides:       python3.8dist(setuptools) = %{version}

%description
Setuptools is a collection of enhancements to the Python 3 distutils that allow
you to more easily build and distribute Python 3 packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources

%prep
%setup -n setuptools-%{version}

%build
python3 bootstrap.py
python3 setup.py build

%install
python3 setup.py install --skip-build --root %{buildroot}

# Remove unused stuff
find %{buildroot}%{_libdir} -name '*.pyc' -delete
find %{buildroot}%{_libdir} -name '*.pyo' -delete
find %{buildroot}%{_libdir} -name '*.o' -delete

%post
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%license LICENSE
%doc docs/* CHANGES.rst README.rst
%{python3_sitelib}/easy_install.py
%{python3_sitelib}/pkg_resources/
%{python3_sitelib}/setuptools*/
%{python3_sitelib}/_distutils_hack/
%{python3_sitelib}/distutils-precedence.pth
%{_bindir}/easy_install
%{_bindir}/easy_install-3.8

%changelog
*   Wed Sep 16 2020 Susant Sahani <ssahaniv@vmware.com> 50.3.0-1
-   Initial rpm release.
