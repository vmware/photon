#
# spec file for package python3-linux-procfs
#

%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-linux-procfs
Version:        0.6.1
Release:        1%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
License:        GPLv2
Summary:        Linux /proc abstraction classes
URL:            https://git.kernel.org/pub/scm/libs/python/python-linux-procfs/python-linux-procfs.git/
Source:         https://cdn.kernel.org/pub/software/libs/python/python-linux-procfs/python-linux-procfs-%{version}.tar.xz
%define sha1 python-linux-procfs=24b8dcc897241b64035f5a77848908456b42011c

BuildArch:     noarch
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-defusedxml

%if %{with_check}
BuildRequires: python3-six
%endif

%description
Abstractions to extract information from the Linux kernel /proc files.

%prep
%autosetup -n python-linux-procfs-%{version}

%build
python3 setup.py build

%install
rm -rf %{buildroot}
python3 setup.py install --skip-build --root %{buildroot}

%check
LANG=en_US.UTF-8 python3 bitmasklist_test.py

%files
%defattr(0755,root,root,0755)
%{_bindir}/pflags
%{python3_sitelib}/procfs/
%defattr(0644,root,root,0755)
%{python3_sitelib}/python_linux_procfs*.egg-info
%license COPYING

%changelog
*   Thu Mar 19 2020 Shreyas B. <shreyasb@vmware.com> 0.6.1-1
-   Initial version.
