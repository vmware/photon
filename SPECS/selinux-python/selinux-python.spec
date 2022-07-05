Summary:        SELinux policy core utilities
Name:           selinux-python
Version:        3.3
Release:        1%{?dist}
License:        Public Domain
Group:          System Environment/Libraries
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha1    %{name}=45dd2f295a4188117469227211cd4a7774dd1ab9

BuildRequires:  python3-devel
BuildRequires:  libsepol-devel = %{version}
BuildRequires:  libselinux-devel = %{version}

%description
The %{name} package contains the management tools use to manage an SELinux environment.

%prep
%autosetup -p1

%build
make %{?_smp_mflags}

%install
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" \
     BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" %{?_smp_mflags} install

rm -rf %{buildroot}%{_mandir}/ru

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_sbindir}/*
%{python3_sitelib}/*
%{_datadir}/bash-completion/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%exclude %{_sharedstatedir}/sepolgen/perm_map

%changelog
* Fri Apr 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3-1
- Initial version.
