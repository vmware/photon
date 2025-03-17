Summary:        Query Language for JSON
Name:           python3-jmespath
Version:        1.0.1
Release:        3%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/jmespath
Source0:        https://pypi.python.org/packages/e5/21/795b7549397735e911b032f255cff5fb0de58f96da794274660bca4f58ef/jmespath-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if 0%{?with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
%endif
Requires:       python3
Requires:       python3-libs
BuildArch:      noarch
Provides:       python%{python3_version}dist(jmespath)

%description
JMESPath (pronounced “james path”) allows you to declaratively specify how to extract elements from a JSON document.

%prep
%autosetup -n jmespath-%{version}

%build
%py3_build

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.0.1-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.1-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.1-1
- Automatic Version Bump
* Wed Jul 21 2021 Tapas Kundu <tkundu@vmware.com> 0.10.0-3
- Added provides
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.10.0-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.10.0-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.9.3-3
- Mass removal python2
* Wed Nov 28 2018 Tapas Kundu <tkundu@vmware.com> 0.9.3-2
- Fix make check
- moved the build requires from subpackages
* Sun Jan 07 2018 Kumar Kaushik <kaushikk@vmware.com> 0.9.3-1
- Initial packaging for photon.
