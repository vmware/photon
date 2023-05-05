Summary:        Extensions to the standard Python datetime module
Name:           python3-setuptools
Version:        65.5.1
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/setuptools/
Source0:        https://files.pythonhosted.org/packages/5f/36/7374297692bb9dbd7569a0f84887c7e5e314c41d5d9518cb76fbb130620d/setuptools-%{version}.tar.gz
%define sha512 setuptools=e75eb7fdb0bc5ffdc76ed864cf753c2672d097a60f8747ac5cd40a49276d33df31fb619877234b4c22693b627d9978ecdd48a5c6c48aa0bbb856d48dec70fb0a
BuildRequires:  python3-devel
BuildRequires:  python3-xml
Requires:       python3
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
* Tue Feb 07 2023 Prashant S Chauhan <psinghchauha@vmware.com> 65.5.1-1
- Separate python3-setuptools from python3.
