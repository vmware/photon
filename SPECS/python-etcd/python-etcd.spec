%define srcname python-etcd

Name:           python3-etcd
Version:        0.4.5
Release:        9%{?dist}
Summary:        Python API for etcd
Group:          Development/Languages/Python
Url:            https://github.com/jplana/python-etcd
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/jplana/python-etcd/archive/refs/tags/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0: auth-api-compatibility.patch

BuildRequires: python3-devel
BuildRequires: python3-setuptools

%if 0%{?with_check}
BuildRequires: python3-pip
BuildRequires: python3-mock
BuildRequires: python3-dnspython
BuildRequires: python3-urllib3
BuildRequires: python3-pyOpenSSL
BuildRequires: etcd
BuildRequires: openssl-devel
BuildRequires: curl-devel
BuildRequires: libffi-devel
%endif

Requires: python3
Requires: python3-setuptools
Requires: python3-dnspython
Requires: python3-urllib3

BuildArch: noarch

%description
Python API for etcd

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
pip3 install nose
python3 setup.py test
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.4.5-9
- Release bump for SRP compliance
* Tue Aug 06 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.4.5-8
- Bump up as part of python3-urllib3 update
* Thu Jul 25 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.4.5-7
- Bump up as part of dnspython update
* Fri Mar 08 2024 Anmol Jain <anmol.jain@broadcom.com> 0.4.5-6
- Bump version as a part of etcd upgrade
* Wed Aug 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.4.5-5
- Add python3-dnspython to requires
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.4.5-4
- openssl 1.1.1
* Thu Jun 18 2020 Tapas Kundu <tkundu@vmware.com> 0.4.5-3
- Mass removal python2
* Tue Dec 04 2018 Ashwin H<ashwinh@vmware.com> 0.4.5-2
- Add %check
* Sat Aug 26 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.4.5-1
- Initial version of python etcd for PhotonOS.
