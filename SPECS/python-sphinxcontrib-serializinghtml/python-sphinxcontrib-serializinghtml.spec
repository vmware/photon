Name:           python3-sphinxcontrib-serializinghtml
Version:        1.1.5
Release:        1%{?dist}
Summary:        A platform independent file lock
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/sphinxcontrib-serializinghtml

Source0: https://files.pythonhosted.org/packages/ac/86/021876a9dd4eac9dae0b1d454d848acbd56d5574d350d0f835043b5ac2cd/sphinxcontrib-serializinghtml-%{version}.tar.gz
%define sha512 sphinxcontrib-serializinghtml=c5aabe4d29fd0455c269f8054089fdd61e1de5c35aa407740fc3baae4cfb3235d9fd5515c0489b0becd12abc8f18d0f42aa169ed315c00f30ba87e64ce851667

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools

%if 0%{?with_check}
BuildRequires: python3-sphinx
BuildRequires: python3-pytest
%endif

Requires:       python3

Provides: python3.9dist(sphinxcontrib-serializinghtml)

%description
This package contains a single module, which implements a platform independent
file locking mechanism for Python.

The lock includes a lock counter and is thread safe. This means, when locking
the same lock object twice, it will not block.

%prep
%autosetup -p1 -n sphinxcontrib-serializinghtml-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
%pytest
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%license LICENSE
%doc README.rst
%{python3_sitelib}/sphinxcontrib/

%changelog
* Mon Sep 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.5-1
- Upgrade to v1.1.5
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.1.4-1
- initial version
