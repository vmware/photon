%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%define debug_package %{nil}

Summary:        Distro - an OS platform information API
Name:           python-distro
Version:        1.5.0
Release:        1%{?dist}
License:        ASL
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/distro
Source0:        https://files.pythonhosted.org/packages/ca/e3/78443d739d7efeea86cbbe0216511d29b2f5ca8dbf51a6f2898432738987/distro-%{version}.tar.gz
%define sha1    distro=cb0e7d550a3c66c960a1914718e4f4dfe1228a19

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:  python-pip
%endif
Requires:       photon-release
Requires:       python2
Requires:       python2-libs
BuildArch:      noarch

%description
Distro provides information about the OS distribution it runs on, such as a reliable machine-readable ID, or version information.

%prep
%setup -q -n distro-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
pip install tox
tox

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*
%doc CHANGELOG.md CONTRIBUTORS.md README.md
%license LICENSE
/usr/bin/*

%changelog
*   Sat Mar 06 2021 Tapas Kundu <tkundu@vmware.com> 1.5.0-1
-   Update to 1.5.0
*   Thu Jul 11 2019 Tapas Kundu <tkundu@vmware.com> 1.4.0-2
-   Updated to build python2 distro pkg.
-   Separated spec file for python3-distro.
*   Tue Feb 12 2019 Tapas Kundu <tkundu@vmware.com> 1.4.0-1
-   Initial packaging for Photon
