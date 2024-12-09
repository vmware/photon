#
# spec file for package python3-linux-procfs
#

Name:           python3-linux-procfs
Version:        0.7.0
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Summary:        Linux /proc abstraction classes
URL:            https://git.kernel.org/pub/scm/libs/python/python-linux-procfs/python-linux-procfs.git/
Source0:        https://cdn.kernel.org/pub/software/libs/python/python-linux-procfs/python-linux-procfs-%{version}.tar.xz
%define sha512  python-linux-procfs=9b2489b47949560245fb23eefa1600869618921173a94534af4db88938fbc855ce37e24100286bdee9fd18a3f140fb86bef06fa7a473ed55e5cdde721f54113c

Source1: license.txt
%include %{SOURCE1}

BuildArch:     noarch
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-defusedxml

%if 0%{?with_check}
BuildRequires: python3-six
%endif

%description
Abstractions to extract information from the Linux kernel /proc files.

%prep
%autosetup -n python-linux-procfs-%{version}

%build
%py3_build

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.7.0-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.7.0-1
- Automatic Version Bump
* Thu Mar 19 2020 Shreyas B. <shreyasb@vmware.com> 0.6.1-1
- Initial version.
