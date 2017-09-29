# FIXME: noarch or generate debuginfo
%define debug_package %{nil}

%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        ANother Tool for Language Recognition
Name:           python-antlrpythonruntime
Version:        3.1.2
Release:        1%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://www.antlr3.org/download/Python/antlr_python_runtime-%{version}.tar.gz
Source0:        antlr_python_runtime-%{version}.tar.gz
%define sha1    antlr_python_runtime=c57d4a03f80d157e9c0c1c8cd3038171900a364c

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python2-devel

Requires:       python2
Requires:       python2-libs

%description
ANother Tool for Language Recognition, is a language tool that provides a framework for constructing recognizers, interpreters, compilers, and translators from grammatical descriptions containing actions in a variety of target languages.

%prep
%setup -q -n antlr_python_runtime-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install py
python2 setup.py test
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%changelog
*   Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 3.1.2-1
-   Initial packaging for Photon
