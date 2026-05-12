%global build_if %{photon_subrelease} <= 91

Summary:        SELinux python3 bindings for libselinux
Name:           libselinux-python3
Version:        3.4
Release:        6.3%{?dist}
Group:          Development/Libraries
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/libselinux-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Source2: libselinux.patches
%include %{SOURCE2}

BuildRequires:  libsepol-devel = %{version}
BuildRequires:  libselinux = %{version}-%{release}
BuildRequires:  pcre2-devel
BuildRequires:  swig
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-devel
Requires:       python3
Requires:       libselinux = %{version}-%{release}

%description
The libselinux-python3 package contains the python3 bindings for developing
SELinux applications.

%prep
%autosetup -p1 -n libselinux-%{version}

%build
make %{?_smp_mflags} \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir} \
  SHLIBDIR=%{_lib} \
  PYTHON=python3 \
  pywrap

%install
# make doesn't support _smp_mflags
make \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir} \
  SHLIBDIR=%{_lib} \
  DESTDIR="%{buildroot}" \
  install-pywrap

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Mon May 11 2026 Bo Gan <bo.gan@broadcom.com> 3.4-6.3
- Add missing libsepol-devel build dependency
* Tue Apr 14 2026 Bo Gan <bo.gan@broadcom.com> 3.4-6.2
- Split python3 sub-package into separate .spec file
