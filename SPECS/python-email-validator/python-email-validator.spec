Summary:        A robust email syntax and deliverability validation library
Name:           python3-email-validator
Version:        1.2.1
Release:        3%{?dist}
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/JoshData/python-email-validator

Source0:        https://github.com/JoshData/python-email-validator/archive/refs/tags/email_validator-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_check}
BuildRequires:  python3-dnspython
BuildRequires:  python3-pytest
BuildRequires:  python3-idna
%endif

Requires:       python3
Requires:       python3-dnspython

%description
This library validates that address are of the form x@y.com. This is the sort
of validation you would want for a login form on a website.

%prep
%autosetup -n python-email-validator-%{version} -p1

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
export PYTHONPATH=%{buildroot}%{python3_sitelib}
pytest -v
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/email_validator
%{python3_sitelib}/email_validator/
%{python3_sitelib}/email_validator-%{version}-py%{python3_version}.egg-info

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.2.1-3
- Release bump for SRP compliance
* Thu Jul 25 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.2.1-2
- Bump up as part of dnspython update
* Wed Oct 12 2022 Nitesh Kumar <kunitesh@vmware.com> 1.2.1-1
- Initial version,Needed by python3-pydantic
