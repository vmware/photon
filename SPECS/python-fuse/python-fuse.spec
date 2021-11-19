Name:           python3-fuse
Version:        1.0.2
Release:        2%{?dist}
Summary:        Python interface to libfuse
License:        LGPL
Group:          Development/Languages/Python
Url:            https://github.com/libfuse/%{name}/archive/%{version}.tar.gz
Source0:        python-fuse-%{version}.tar.gz
%define sha1    python-fuse=f01919b521bae353d2819cdc62bd54e0711c7a7f
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  fuse
BuildRequires:  fuse-devel
BuildRequires:  pkg-config
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pip
%endif
Requires:       fuse
Requires:       python3
Requires:       python3-libs

%description
FUSE (Filesystem in USErspace) is a simple interface for userspace programs to export a virtual filesystem to the linux kernel. "fuse.py" reexports the root filesystem within the mount point. It also offers a class, fuse.Fuse, which can be subclassed to create a filesystem.

%prep
%autosetup -n python-fuse-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --skip-build
find %{buildroot}%{_libdir} -name '*.pyc' -delete

%check
pip3 install py

%files
%defattr(-,root,root,-)
%{python3_sitelib}/fuse*

%changelog
*   Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.2-2
-   Update release to compile with python 3.10
*   Thu Feb 18 2021 Tapas Kundu <tkundu@vmware.com> 1.0.2-1
-   Initial packaging for python3-fuse
