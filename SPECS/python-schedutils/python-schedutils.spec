#
# spec file for package python3-schedutils
#

Name:           python3-schedutils
Summary:        Linux scheduler python bindings
Version:        0.6
Release:        4%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://git.kernel.org/pub/scm/libs/python/python-schedutils/python-schedutils.git/
Source0:         https://cdn.kernel.org/pub/software/libs/python/python-schedutils/python-schedutils-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  gcc

%description
Python interface for the Linux scheduler sched_{get,set}{affinity,scheduler}\
functions and friends.

%prep
%autosetup -n python-schedutils-%{version}

%build
%py3_build

%install
python3 setup.py install --skip-build --root %{buildroot}

%files
%defattr(0755,root,root,0755)
%license COPYING
%{_bindir}/pchrt
%{_bindir}/ptaskset
%{_mandir}/man1/pchrt.1*
%{_mandir}/man1/ptaskset.1*
%{python3_sitearch}/schedutils*.so
%{python3_sitearch}/*.egg-info

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.6-4
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.6-3
- Update release to compile with python 3.11
* Thu May 28 2020 Shreyas B. <shreyasb@vmware.com> 0.6-2
- Remove BuildArch.
* Thu Mar 19 2020 Shreyas B. <shreyasb@vmware.com> 0.6-1
- Initial version.
