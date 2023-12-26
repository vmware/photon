%define srcname sphinxcontrib-serializinghtml

Name:           python3-sphinxcontrib-serializinghtml
Version:        1.1.5
Release:        1%{?dist}
Summary:        Sphinx extension for serialized HTML
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/sphinxcontrib-serializinghtml

Source0: https://files.pythonhosted.org/packages/ac/86/021876a9dd4eac9dae0b1d454d848acbd56d5574d350d0f835043b5ac2cd/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=c5aabe4d29fd0455c269f8054089fdd61e1de5c35aa407740fc3baae4cfb3235d9fd5515c0489b0becd12abc8f18d0f42aa169ed315c00f30ba87e64ce851667

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools

Requires: python3

Provides: python%{python3_version}dist(%{srcname})

%description
sphinxcontrib-serializinghtml is a sphinx extension which outputs "serialized"
HTML files (json and pickle).

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%license LICENSE
%doc README.rst

%changelog
* Mon Jan 08 2024 Nitesh Kumar <kunitesh@vmware.com> 1.1.5-1
- Upgrade version as required by python3-sphinx v5.1.1
* Sun Aug 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.4-3
- Fix summary & description
* Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.1.4-2
- Update release to compile with python 3.10
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.1.4-1
- initial version
