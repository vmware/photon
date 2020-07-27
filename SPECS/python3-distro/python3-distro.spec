%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%define debug_package %{nil}

Summary:        Distro - an OS platform information API
Name:           python3-distro
Version:        1.5.0
Release:        1%{?dist}
License:        ASL
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/distro
Source0:        https://files.pythonhosted.org/packages/ca/e3/78443d739d7efeea86cbbe0216511d29b2f5ca8dbf51a6f2898432738987/distro-%{version}.tar.gz
%define sha1    distro=cb0e7d550a3c66c960a1914718e4f4dfe1228a19

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python3-pip
%endif
Requires:       photon-release
Requires:       python3
Requires:       python3-libs
BuildArch:      noarch
Obsoletes:      python-distro
%description
Distro provides information about the OS distribution it runs on, such as a reliable machine-readable ID, or version information.

%prep
%setup -q -n distro-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
pip3 install tox
tox

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%doc CHANGELOG.md CONTRIBUTORS.md README.md
%license LICENSE
/usr/bin/*

%changelog
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.0-1
-   Automatic Version Bump
*   Wed Jul 24 2019 Tapas Kundu <tkundu@vmware.com> 1.4.0-3
-   Obsolete python-distro
*   Thu Jul 11 2019 Tapas Kundu <tkundu@vmware.com> 1.4.0-2
-   Separate spec file for python3-distro package in Photon
