Summary:        Extensions to the standard Python datetime module
Name:           python3-setuptools
Version:        57.4.0
Release:        2%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/setuptools/
Source0:        https://files.pythonhosted.org/packages/db/e2/c0ced9ccffb61432305665c22842ea120c0f649eec47ecf2a45c596707c4/setuptools-57.4.0.tar.gz
%define sha512 setuptools=7fcc297ea3e6310f2ec8ba5bf0d509e3f4acbce6bde7e5f0fe1b022c147cf88a047471bd4aa278724e86ebc6be800015fb935c7a31dbb6a0801a2d380ddd89f2
# if you make any security fix in this package, package the whl files
# python3.spec without miss
Patch0:         CVE-2022-40897.patch
Patch1:         CVE-2024-6345.patch
BuildRequires:  python3-devel
BuildRequires:  python3-xml
Requires:       python3 >= 3.7.5-25
Requires:       python3-xml
BuildArch:      noarch
Provides:       python%{python3_version}dist(setuptools)

%description
Setuptools is a fully-featured, actively-maintained, and stable library designed to facilitate packaging Python projects.
It helps developers to easily share reusable code (in the form of a library) and programs
(e.g., CLI/GUI tools implemented in Python), that can be installed with pip and uploaded to PyPI.

%prep
%autosetup -p1 -n setuptools-%{version}

%build
%{py3_build}

%install
%{py3_install}
find %{buildroot}%{python3_sitelib} -name '*.exe' | xargs rm -f

%check
%{py3_test}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 755)
%{python3_sitelib}/*

%changelog
* Thu Aug 22 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 57.4.0-2
- Fix CVE-2024-6345
* Tue Feb 07 2023 Prashant S Chauhan <psinghchauha@vmware.com> 57.4.0-1
- Separate python3-setuptools from python3.
- Update to latest Fix CVE-2022-40897
