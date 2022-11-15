Name:           python3-fuse
Version:        1.0.2
Release:        1%{?dist}
Summary:        Python interface to libfuse
License:        LGPL
Group:          Development/Languages/Python
URL:            https://github.com/libfuse/python-fuse
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/libfuse/python-fuse/archive/refs/tags/python-fuse-%{version}.tar.gz
%define sha512 python-fuse=9c71e621db41ea70fe0cf824df73b81704f08f38470b6cddd2d7c5933c90edd80af86a0aa20f19e0e4e4aec1dde1c49b65646931cf7debdc5dc875cb3e2d1c31

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
* Thu Feb 18 2021 Tapas Kundu <tkundu@vmware.com> 1.0.2-1
- Initial packaging for python3-fuse
