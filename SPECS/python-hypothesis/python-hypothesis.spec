%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-hypothesis
Version:        5.23.2
Release:        1%{?dist}
Summary:        Python library for creating unit tests which are simpler to write and more powerful
License:        MPLv2.0
Group:          Development/Languages/Python
Url:            https://github.com/HypothesisWorks/hypothesis-python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/cf/d5/b3d491e4b5094be0ef69b910d637096c8e23f84a9bdc4eba0b869220d1f0/hypothesis-%{version}.tar.gz
%define sha1    hypothesis=756788bf624afb5d9cf6a3d13aaa510926ddc073
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
Hypothesis is an advanced testing library for Python. It lets you write tests which are parametrized by a source of examples,
and then generates simple and comprehensible examples that make your tests fail. This lets you find more bugs in your code with less work

%prep
%setup -n hypothesis-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 5.23.2-1
-   Automatic Version Bump
*   Wed Jun 17 2020 Tapas Kundu <tkundu@vmware.com> 3.71.0-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.71.0-1
-   Update to version 3.71.0
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.8.2-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.8.2-2
-   Changed python to python2
*   Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.8.2-1
-   Initial
