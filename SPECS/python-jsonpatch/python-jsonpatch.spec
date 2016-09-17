Name:           python-jsonpatch
Version:        1.9
Release:        3%{?dist}
Summary:        Applying JSON Patches in Python
License:        Modified BSD License
Group:          Development/Languages/Python
Url:            https://pypi.python.org/packages/source/j/jsonpatch/jsonpatch-%{version}.tar.gz
Source0:        jsonpatch-%{version}.tar.gz
%define sha1 jsonpatch=b45d37d581315e423451a9f0ea8dc091b6138254

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python-setuptools
BuildRequires: python-jsonpointer
Requires: python-jsonpointer

BuildArch:      noarch

%description
Library to apply JSON Patches according to RFC 6902.

%prep
%setup -n jsonpatch-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python ext_tests.py && python tests.py

%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%{_bindir}/jsondiff
%{_bindir}/jsonpatch

%changelog
*       Mon Oct 04 2016 ChangLee <changlee@vmware.com> 1.9-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9-2
-	GA - Bump release of all rpms
* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
