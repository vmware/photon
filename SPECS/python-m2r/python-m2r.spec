%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Markdown to reStructuredText converter.
Name:           python-m2r
Version:        0.2.0
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/m2r
Source0:        https://github.com/miyakogi/m2r/archive/v%{version}/m2r-%{version}.tar.gz
%define sha1    m2r=a8da99cfb8d964fbd1404eff8fe3782dfa2ff3a6

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-mistune
BuildRequires:  python-docutils
%if %{with_check}
BuildRequires:  python-Pygments
%endif

Requires:       python2
Requires:       python2-libs
Requires:       python-mistune
Requires:       python-docutils

BuildArch:      noarch

%description
M2R converts a markdown file including reST markups to a valid reST format.

Why another converter?

I wanted to write sphinx document in markdown, since it’s widely used now and easy to write code blocks and lists. However, converters using pandoc or recommonmark do not support many reST markups and sphinx extensions. For example, reST’s reference link like see `ref`_ (this is very convenient in long document in which same link appears multiple times) will be converted to a code block in HTML like see <code>ref</code>_, which is not expected.

%package -n     python3-m2r
Summary:        python-m2r
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-mistune
BuildRequires:  python3-docutils
%if %{with_check}
BuildRequires:  python3-Pygments
%endif

Requires:       python3
Requires:       python3-libs
Requires:       python3-mistune
Requires:       python3-docutils

%description -n python3-m2r
Python 3 version.

%prep
%setup -q -n m2r-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/m2r %{buildroot}/%{_bindir}/m2r3
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 mock
python2 setup.py test -s tests
pushd ../p3dir
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 mock
python3 setup.py test -s tests
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*
%{_bindir}/m2r

%files -n python3-m2r
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/m2r3

%changelog
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.2.0-1
-   Update to version 0.2.0
*   Fri Jul 21 2017 Divya Thaluru <dthaluru@vmware.com> 0.1.7-1
-   Updated version to 0.1.7
-   Fixed make check errors
*   Mon Jun 19 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.5-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.1.5-2
-   Separate the python2 and python3 scripts in the bin directory
*   Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.5-1
-   Initial packaging for Photon
