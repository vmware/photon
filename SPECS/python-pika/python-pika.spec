Name:           python3-pika
Version:        1.2.1
Release:        2%{?dist}
Summary:        Pika is a RabbitMQ (AMQP 0-9-1) client library for Python.
Group:          Development/Languages/Python
URL:            https://github.com/pika/pika
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/pika/pika/archive/refs/tags/pika-1.2.1.tar.gz
%define sha512  pika=2688f8f04990c25a5cb6f6bea4f3407bbf35fca9060e24ab4dc181f829bf4fe7d76d46f35947c8cb1f040ec880effc6e62d7303ec418eb703d51dc7a1a96d72d

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.2.1-2
- Release bump for SRP compliance
* Mon Sep 11 2023 Felippe Burkf <burkf@vmware.com> 1.2.1-1
- Initial Build 1.2.1
