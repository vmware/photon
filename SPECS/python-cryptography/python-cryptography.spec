Summary:        Python cryptography library
Name:           python-cryptography
Version:        1.1
Release:        1%{?dist}
Url:            https://cryptography.io
License:        ASL 2.0
Group:          Development/Languages/Python
Source0:        https://pypi.python.org/packages/source/c/cryptography/cryptography-%{version}.tar.gz
%define sha1 cryptography=e04eb5febd7d127bc673504a18984daf4491e941

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python2-devel
BuildRequires: python-setuptools
Requires:      python-cffi
BuildRequires: python-cffi
BuildRequires: openssl-devel
Requires:      openssl

Requires:       python2
Requires:       python2-libs

%description
Cryptography is a Python library which exposes cryptographic recipes and primitives.


%prep
%setup -q -n cryptography-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}/*

%changelog
* Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> 1.1-1
- Initial packaging for Photon
