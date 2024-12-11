Summary:        Amazon Web Services Library.
Name:           python3-boto
Version:        2.49.0
Release:        4%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/boto/boto

Source0: https://files.pythonhosted.org/packages/source/b/boto/boto-%{version}.tar.gz
%define sha512 boto=2175cf30cd25bbc05812e83e5ade7668c3e21b1bb09aa1b43f0f0ac7d6967a646394fb52c9be673ebb65618c5b33a52d6f31f6da702f5cd1d6c9a18169476dd4

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

%if 0%{?with_check}
Patch0:         makecheck.patch
BuildRequires:  python3-requests
BuildRequires:  python3-pip
%endif

Requires:       python3
Requires:       python3-requests
Requires:       python3-xml

BuildArch:      noarch

%description
Boto is a Python package that provides interfaces to Amazon Web Services. Currently, all features work with Python 2.6 and 2.7. Work is under way to support Python 3.3+ in the same codebase. Modules are being ported one at a time with the help of the open source community, so please check below for compatibility with Python 3.3+.

%prep
%autosetup -p1 -n boto-%{version}

%build
%py3_build

%install
%py3_install -- --single-version-externally-managed
for item in %{buildroot}%{_bindir}/*; do
  mv ${item} "${item}-%{python3_version}"
done

%if 0%{?with_check}
%check
# nose is not maintained anymore
#pip3 install nose httpretty mock
#python3 ./tests/test.py unit
%endif

%files
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/asadmin-%{python3_version}
%{_bindir}/bundle_image-%{python3_version}
%{_bindir}/cfadmin-%{python3_version}
%{_bindir}/cq-%{python3_version}
%{_bindir}/cwutil-%{python3_version}
%{_bindir}/dynamodb_dump-%{python3_version}
%{_bindir}/dynamodb_load-%{python3_version}
%{_bindir}/elbadmin-%{python3_version}
%{_bindir}/fetch_file-%{python3_version}
%{_bindir}/glacier-%{python3_version}
%{_bindir}/instance_events-%{python3_version}
%{_bindir}/kill_instance-%{python3_version}
%{_bindir}/launch_instance-%{python3_version}
%{_bindir}/list_instances-%{python3_version}
%{_bindir}/lss3-%{python3_version}
%{_bindir}/mturk-%{python3_version}
%{_bindir}/pyami_sendmail-%{python3_version}
%{_bindir}/route53-%{python3_version}
%{_bindir}/s3put-%{python3_version}
%{_bindir}/sdbadmin-%{python3_version}
%{_bindir}/taskadmin-%{python3_version}

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.49.0-4
- Release bump for SRP compliance
* Wed Feb 17 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.49.0-3
- Fix makecheck
* Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 2.49.0-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.49.0-1
- Update to version 2.49.0
* Tue Sep 12 2017 Xiaolin Li <xiaolinl@vmware.com> 2.48.0-1
- Initial packaging for Photon
