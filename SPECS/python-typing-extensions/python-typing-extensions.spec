Name:           python3-typing-extensions
Version:        4.3.0
Release:        1%{?dist}
Summary:        Backported and Experimental Type Hints for Python 3.7+
License:        PSF
Group:          Development/Tools
Url:            https://pypi.org/project/typing-extensions
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/9e/1d/d128169ff58c501059330f1ad96ed62b79114a2eb30b8238af63a2e27f70/typing_extensions-4.3.0.tar.gz
%define sha512  typing_extensions=69e4a393aaaaa45d20f32027cc35c77a950bf1f9b82f0eb2906a4b466eb319b867b5f53c0afc71ca613817d7e37d305fe73c50e93b1d4b389fdb8f1e4d5f8535

Patch0:         python-typing-extensions-check.patch
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-test
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
Typing defines a standard notation for Python function and variable type annotations. The notation can be used for documenting code in a concise,
standard format, and it has been designed to also be used by static and runtime type checkers, static analyzers, IDEs and other tools.

%prep
%autosetup -n typing_extensions-%{version} -p1

%build
python3 -m pip wheel --disable-pip-version-check --verbose .

%install
python3 -m pip install --root %{buildroot} --prefix %{_prefix} --disable-pip-version-check --verbose .

%check
python3 ./src/test_typing_extensions.py

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Thu Aug 11 2022 Tapas Kundu <tkundu@vmware.com> 4.3.0-1
-   Update to version 4.3.0
