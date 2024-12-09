Name:           python3-fuse
Version:        1.0.5
Release:        2%{?dist}
Summary:        Python interface to libfuse
Group:          Development/Languages/Python
Url:            https://github.com/libfuse/%{name}/archive/%{version}.tar.gz
Source0: https://github.com/libfuse/python-fuse/archive/refs/tags/python-fuse-%{version}.tar.gz
%define sha512  python-fuse=e0d0cc0f3dee9416eefe430119e8f2f5a9bbc88a214d36d1d23c7e1f7ce78cc977a173f6d22c05cb928715d5c657ba29738f60453323b25299dddc08d57595d2

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  fuse-devel
BuildRequires:  pkg-config
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       fuse
Requires:       python3

%description
FUSE (Filesystem in USErspace) is a simple interface for userspace programs to export a virtual filesystem to the linux kernel. "fuse.py" reexports the root filesystem within the mount point. It also offers a class, fuse.Fuse, which can be subclassed to create a filesystem.

%prep
%autosetup -p1 -n python-fuse-%{version}

%build
%py3_build

%install
%py3_install
find %{buildroot}%{_libdir} -name '*.pyc' -delete

%files
%defattr(-,root,root,-)
%{python3_sitelib}/fuse*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.0.5-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.5-1
- Automatic Version Bump
* Thu Feb 18 2021 Tapas Kundu <tkundu@vmware.com> 1.0.2-1
- Initial packaging for python3-fuse
