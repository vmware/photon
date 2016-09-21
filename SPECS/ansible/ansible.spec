Summary:        Configuration-management, application deployment, cloud provisioning system
Name:           ansible
Version:        2.1.1.0
Release:        1%{?dist}
License:        GPLv3+
URL:            https://www.ansible.com
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://releases.ansible.com/ansible/%{name}-%{version}.tar.gz
%define sha1 ansible=f596a7950ebe839eaf650643e9afeb8c1307817a

BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

%description
Ansible is a radically simple IT automation system. It handles configuration-management, application deployment, cloud provisioning, ad-hoc task-execution, and multinode orchestration - including trivializing things like zero downtime rolling updates with load balancers.

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build \
    --root "%{buildroot}"

%check
make test

%files 
%defattr(-, root, root)
%{_bindir}/*
%{python_sitelib}/*

%changelog
*   Wed Sep 21 2016 Xiaolin Li <xiaolinl@vmware.com> 2..1.1.0-1
-   Initial build. First version
