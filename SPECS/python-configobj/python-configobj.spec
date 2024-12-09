Name:           python3-configobj
Version:        5.0.6
Release:        7%{?dist}
Summary:        Config file reading, writing and validation
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://configobj.readthedocs.io/en/latest

Source0: https://github.com/DiffSK/configobj/archive/refs/tags/configobj-%{version}.tar.gz
%define sha512 configobj=f253fdd0bc3fcd37f56c9ceb28f5c8c739b0861e099b07a3929645907c97b2261f0529850a95c1a42507846f72d88a0992fcd1e1d6fa8654dc713d120f769963

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-six

BuildArch:      noarch

%description
ConfigObj is a simple but powerful config file reader and writer: an ini file round tripper. Its main feature is that it is very easy to use, with a straightforward programmer’s interface and a simple syntax for config files.

%prep
%autosetup -p1 -n configobj-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 validate.py

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.0.6-7
- Release bump for SRP compliance
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 5.0.6-6
- Update release to compile with python 3.11
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 5.0.6-5
- Mass removal python2
* Mon May 15 2017 Kumar Kaushik <kaushikk@vmware.com> 5.0.6-4
- Adding python 3 support.
* Mon Oct 03 2016 ChangLee <changLee@vmware.com> 5.0.6-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.0.6-2
- GA - Bump release of all rpms
* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
