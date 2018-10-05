%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        ANother Tool for Language Recognition
Name:           python-antlrpythonruntime
Version:        3.1.3
Release:        2%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://www.antlr3.org/download/Python/antlr_python_runtime-%{version}.tar.gz
Source0:        antlr_python_runtime-%{version}.tar.gz
%define sha1    antlr_python_runtime=dc095863a254cdf9606784dbd6efb43cf56a6804

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  lapack-devel

Requires:       python2
Requires:       python2-libs
BuildArch:      noarch

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

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%changelog
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.3-2
-   Fix arch
*   Wed Mar 29 2017 Rongrong Qiu <rqiu@vmware.com> 3.1.3-1
-   upgrade to 3.1.3
*   Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 3.1.2-1
-   Initial packaging for Photon
