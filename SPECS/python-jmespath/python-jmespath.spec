%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Summary:        Query Language for JSON
Name:           python3-jmespath
Version:        0.10.0
Release:        2%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/jmespath
Source0:        https://pypi.python.org/packages/e5/21/795b7549397735e911b032f255cff5fb0de58f96da794274660bca4f58ef/jmespath-%{version}.tar.gz
%define         sha1 jmespath=356c48dfea2214dd9e7e2b222a99dddfe9c0d05c
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
%endif
Requires:       python3
Requires:       python3-libs
BuildArch:      noarch

%description
JMESPath (pronounced “james path”) allows you to declaratively specify how to extract elements from a JSON document.


%prep
%setup -q -n jmespath-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}
for item in %{buildroot}/%{_bindir}/*
    do mv ${item} "${item}-%{python3_version}" ;
done

%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 nose
python3 setup.py test

%files
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/jp.py-%{python3_version}

%changelog
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.10.0-2
-   openssl 1.1.1
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.10.0-1
-   Automatic Version Bump
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.9.3-3
-   Mass removal python2
*   Wed Nov 28 2018 Tapas Kundu <tkundu@vmware.com> 0.9.3-2
-   Fix make check
-   moved the build requires from subpackages
*   Sun Jan 07 2018 Kumar Kaushik <kaushikk@vmware.com> 0.9.3-1
-   Initial packaging for photon.
