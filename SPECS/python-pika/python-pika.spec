%global build_if %{photon_subrelease} >= 91

Name:           python3-pika
Version:        1.2.1
Release:        4%{?dist}
Summary:        Pika is a RabbitMQ (AMQP 0-9-1) client library for Python.
Group:          Development/Languages/Python
URL:            https://github.com/pika/pika
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/pika/pika/archive/refs/tags/pika-1.2.1.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3
BuildArch:      noarch

%description
Pika is a pure-Python implementation of the AMQP 0-9-1 protocol including RabbitMQ’s extensions.

%prep
%autosetup -n pika-%{version}

%build
%py3_build

%install
%py3_install

%check
%pytest

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%doc README.rst

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.2.1-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.2.1-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.2.1-2
- Release bump for SRP compliance
* Mon Sep 11 2023 Felippe Burkf <burkf@vmware.com> 1.2.1-1
- Initial Build 1.2.1
