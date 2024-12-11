%define srcname Sphinx

Summary:       Python documentation generator
Name:          python3-sphinx
Version:       5.1.1
Release:       4%{?dist}
Group:         Development/Tools
URL:           www.sphinx-doc.org
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: https://github.com/sphinx-doc/sphinx/archive/refs/tags/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=82cb4c435b0f6cee6bf80b81028f06e425e3d6fb5614e64b1f5a8c715ece80b697b5b55e04f3afe26236bb4590de9cd41008d6480c4b3d895803d83e914afff3

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-babel
BuildRequires: python3-docutils
BuildRequires: python3-jinja2
BuildRequires: python3-Pygments
BuildRequires: python3-six
BuildRequires: python3-alabaster
BuildRequires: python3-imagesize
BuildRequires: python3-requests
BuildRequires: python3-snowballstemmer
BuildRequires: python3-typing
BuildRequires: python3-packaging
BuildRequires: python3-sphinxcontrib-applehelp
BuildRequires: python3-sphinxcontrib-devhelp
BuildRequires: python3-sphinxcontrib-qthelp
BuildRequires: python3-sphinxcontrib-htmlhelp
BuildRequires: python3-sphinxcontrib-jsmath
BuildRequires: python3-sphinxcontrib-serializinghtml

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-pip
%endif

Requires: python3-sphinxcontrib-applehelp
Requires: python3-sphinxcontrib-devhelp
Requires: python3-sphinxcontrib-qthelp
Requires: python3-sphinxcontrib-htmlhelp
Requires: python3-sphinxcontrib-jsmath
Requires: python3-sphinxcontrib-serializinghtml
Requires: python3-packaging
Requires: python3
Requires: python3-babel
Requires: python3-docutils
Requires: python3-jinja2
Requires: python3-Pygments
Requires: python3-six
Requires: python3-alabaster
Requires: python3-imagesize
Requires: python3-requests
Requires: python3-snowballstemmer
Requires: python3-typing

BuildArch: noarch

%description
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

for fn in quickstart build autogen apidoc; do
  mv %{buildroot}%{_bindir}/sphinx-${fn} %{buildroot}%{_bindir}/sphinx-${fn}3
  ln -sv sphinx-${fn}3 %{buildroot}%{_bindir}/sphinx-${fn}
done

%check
pip3 install html5lib
%{pytest}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/sphinx-quickstart*
%{_bindir}/sphinx-build*
%{_bindir}/sphinx-autogen*
%{_bindir}/sphinx-apidoc*
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.1.1-4
- Release bump for SRP compliance
* Sun Aug 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.1.1-3
- Fix file packaging
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 5.1.1-2
- Update release to compile with python 3.11
* Mon Sep 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.1.1-1
- Upgrade to v5.1.1
* Thu Oct 28 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.3.0-3
- Bump version as a part of python-babel upgrade
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.3.0-2
- Fix build with new rpm
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 3.3.0-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 3.2.1-1
- Automatic Version Bump
* Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 3.2.0-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1.2-1
- Automatic Version Bump
* Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 1.7.9-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.7.9-1
- Update to version 1.7.9
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.5.3-5
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.5.3-4
- Keep the original python2 scripts and rename the python3 scripts
* Wed Apr 26 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.5.3-3
- BuildRequires and Requires python-babel, python-docutils, python-jinja2,
  python-Pygments, python-six, python-alabaster, python-imagesize,
  python-requests and python-snowballstemmer. Adding python3 version
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.3-2
- Fix arch
* Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 1.5.3-1
- Upgrade version to 1.5.3
* Fri Dec 16 2016 Dheeraj Shetty <dheerajs@vmware.com> 1.5.1-1
- Initial
