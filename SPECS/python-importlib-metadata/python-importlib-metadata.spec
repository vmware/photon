%define srcname importlib_metadata

Summary:        Library to access the metadata for a Python package
Name:           python3-importlib-metadata
Version:        4.13.0
Release:        1%{?dist}
Group:          Development/Languages/Python
License:        ASL 2.0
URL:            https://github.com/python/importlib_metadata
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/55/12/ab288357b884ebc807e3f4eff63ce5ba6b941ba61499071bf19f1bbc7f7f/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=68deb9b017d89df05b613c564bfaafd9024f9a6b1b14973bb75c0756f29911c6a2516a87b4fad60cb15b66bca79a275163fb8db2cfbd088ab952633de056d1e1

BuildArch:     noarch

BuildRequires: python3-devel
BuildRequires: python3-pip

%if 0%{?with_check}
BuildRequires:  python3-test
BuildRequires:  python3-pytest
BuildRequires:  python3-typing-extensions
%endif

Requires:      python3
Requires:      python3-typing-extensions

%description
Library to access the metadata for a Python package.
This package supplies third-party access to the functionality
of importlib.metadata including improvements added to subsequent
Python versions.

%prep
%autosetup -n %{srcname}-%{version}

%build
%{python3} -m pip wheel --disable-pip-version-check --verbose .

%install
%{python3} -m pip install --root %{buildroot} --prefix %{_prefix} --disable-pip-version-check --verbose .

rm -f %{buildroot}%{python3_sitelib}/__pycache__/typing_extensions.cpython-37.pyc \
      %{buildroot}%{python3_sitelib}/typing_extensions.py

%if 0%{?with_check}
%check
pip3 install pluggy more_itertools importlib_resources pyfakefs
%pytest --ignore exercises.py -k "not test_find_local"
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Thu Jan 12 2023 Srish Srinivasan <ssrish@vmware.com> 4.13.0-1
- Initial build. First version
