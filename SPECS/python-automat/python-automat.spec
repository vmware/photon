%define srcname Automat

Summary:        Self-service finite-state machines for the programmer on the go.
Name:           python3-automat
Version:        22.10.0
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/Automat

Source0: https://files.pythonhosted.org/packages/source/A/Automat/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=5819cfe0687bf391949891562f3657f449cf9a8e8ea90c1537e89509dc618da1160856f92ab52dc450e0a7d51d0e4644bfe2db3d4108126a42ee1bea2f06bb7a

BuildRequires: python3-devel
BuildRequires: python3-packaging
BuildRequires: python3-pip
BuildRequires: python3-setuptools_scm
BuildRequires: python3-setuptools
BuildRequires: python3-xml
BuildRequires: python3-docutils
BuildRequires: python3-mistune
BuildRequires: python3-graphviz
BuildRequires: python3-attrs
BuildRequires: python3-six

%if 0%{?with_check}
BuildRequires: python3-pytest
%endif

Requires: python3-six
Requires: python3-attrs
Requires: python3
Requires: python3-graphviz
Requires: python3-Twisted

BuildArch: noarch

%description
Self-service finite-state machines for the programmer on the go.

Automat is a library for concise, idiomatic Python expression of finite-state
automata (particularly deterministic finite-state transducers).

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}
mv %{buildroot}%{_bindir}/automat-visualize \
       %{buildroot}%{_bindir}/automat-visualize3
ln -sv automat-visualize3 %{buildroot}%{_bindir}/automat-visualize

%if 0%{?with_check}
%check
%pytest
%endif

%files
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/automat-visualize*

%changelog
* Sun Aug 13 2023 Shreenidhi Shedi <sshedi@vmware.com> 22.10.0-1
- Upgrade to 22.10.0
- Drop m2r dependency
* Thu Aug 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 20.2.0-4
- Add twisted to requires
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 20.2.0-3
- Update release to compile with python 3.11
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 20.2.0-2
- Fix build with new rpm
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 20.2.0-1
- Automatic Version Bump
* Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 0.7.0-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.7.0-1
- Update to version 0.7.0
* Mon Jul 17 2017 Divya Thaluru <dthaluru@vmware.com> 0.5.0-4
- Fixed run time dependencies
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.5.0-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.5.0-2
- Separate the python3 and python2 scripts in bin directory
* Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 0.5.0-1
- Initial packaging for Photon
