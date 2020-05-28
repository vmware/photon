#
# spec file for package python3-schedutils
#

%{!?python3_sitearch: %define python3_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-schedutils
Summary:        Linux scheduler python bindings
Version:        0.6
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
License:        GPLv2
URL:            https://git.kernel.org/pub/scm/libs/python/python-schedutils/python-schedutils.git/
Source:         https://cdn.kernel.org/pub/software/libs/python/python-schedutils/python-schedutils-%{version}.tar.xz
%define sha1 python-schedutils=48777c044a4b30b99bf2c84d3e2d645010a5e9d4
BuildRequires:  python3-devel
BuildRequires:  gcc

%description
Python interface for the Linux scheduler sched_{get,set}{affinity,scheduler}\
functions and friends.

%prep
%autosetup -n python-schedutils-%{version}

%build
python3 setup.py build

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
*   Thu May 28 2020 Shreyas B. <shreyasb@vmware.com> 0.6-2
-   Remove BuildArch.
*   Thu Mar 19 2020 Shreyas B. <shreyasb@vmware.com> 0.6-1
-   Initial version.
