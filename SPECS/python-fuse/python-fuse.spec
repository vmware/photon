%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-fuse
Version:        0.2.1
Release:        2%{?dist}
Summary:        Python interface to libfuse
License:        LGPL
Group:          Development/Languages/Python
Url:            https://github.com/libfuse/%{name}/archive/%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1    python-fuse=789a922e0c11ed961c469794c73ea7b9ef88eb5f
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  fuse
BuildRequires:  fuse-devel
BuildRequires:  pkg-config
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
Requires:       fuse
Requires:       python2
Requires:       python2-libs

%description
FUSE (Filesystem in USErspace) is a simple interface for userspace programs to export a virtual filesystem to the linux kernel. "fuse.py" reexports the root filesystem within the mount point. It also offers a class, fuse.Fuse, which can be subclassed to create a filesystem.

%prep
%setup -n %{name}-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install py

%files
%defattr(-,root,root,-)
%{python2_sitelib}/fuse*

%changelog
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.2.1-2
-   Change python to python2
*   Thu Apr 06 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.2.1-1
-   Initial version of python-fuse package for Photon.
