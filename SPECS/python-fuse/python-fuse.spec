%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-fuse
Version:        1.0.2
Release:        1%{?dist}
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
Requires:       fuse
Requires:       python3
Requires:       python3-libs

%description
FUSE (Filesystem in USErspace) is a simple interface for userspace programs to export a virtual filesystem to the linux kernel. "fuse.py" reexports the root filesystem within the mount point. It also offers a class, fuse.Fuse, which can be subclassed to create a filesystem.

%prep
%setup -n python-fuse-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --skip-build
find %{buildroot}%{_libdir} -name '*.pyc' -delete

%check
easy_install py

%files
%defattr(-,root,root,-)
%{python3_sitelib}/fuse*

%changelog
*   Thu Feb 18 2021 Tapas Kundu <tkundu@vmware.com> 1.0.2-1
-   Initial packaging for python3-fuse
