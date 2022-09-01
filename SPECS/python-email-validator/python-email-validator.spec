Summary:        A robust email syntax and deliverability validation library
Name:           python3-email-validator
Version:        1.2.1
Release:        1%{?dist}
Group:          Development/Tools
License:        CC0
Vendor:         VMware, Inc.
Distribution:   Photon

URL:            https://pypi.org/project/email-validator
Source0:        https://files.pythonhosted.org/packages/58/be/886a3accc1082c5205e253bebf15a2207b3a5b0b23a5b110d968ea20a94e/email_validator-%{version}.tar.gz
%define sha512  email_validator=c65117a184fe3dcc183a3aef32734b30443dc502348ac68da35bad8297ba5501653275fe73d54a7a429cff1dec85706d4752e50d0f036ef667bdfa5a1cf7b9be
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3-dnspython

%description
This library validates that address are of the form x@y.com. This is the sort
of validation you would want for a login form on a website.

%prep
%autosetup -n email_validator-%{version} -p1

%build
%py3_build

%install
%py3_install

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/email_validator
%{python3_sitelib}/email_validator/
%{python3_sitelib}/email_validator-%{version}-py%{python3_version}.egg-info

%changelog
* Thu Sep 1 2022 Nitesh Kumar <kunitesh@vmware.com> - 1.2.1-1
- Initial version,Needed by python3-pydantic
