Name:           python-jsonpatch
Version:        1.15
Release:        1%{?dist}
Summary:        Applying JSON Patches in Python
License:        Modified BSD License
Group:          Development/Languages/Python
Url:		https://pypi.python.org/pypi/jsonpatch
Source0:        https://pypi.python.org/packages/be/c1/947048a839120acefc13a614280be3289db404901d1a2d49b6310c6d5757/jsonpatch-%{version}.tar.gz
%define sha1 jsonpatch=a678cb3d2a91fc350c7355361f0d3a0d9808d119

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
*       Mon Apr 03 2017 Sarah Choi <sarahc@vmware.com> 1.15-1
-       Update to 1.15
*       Mon Oct 04 2016 ChangLee <changlee@vmware.com> 1.9-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9-2
-	GA - Bump release of all rpms
* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
