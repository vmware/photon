Summary:    File manager
Name:       mc
Version:    4.8.25
Release:    3%{?dist}
License:    GPLv3+
URL:        https://www.midnight-commander.org
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    http://ftp.midnight-commander.orgtar/%{name}-%{version}.tar.xz
%define sha512 %{name}=51913fd41df18b49498b97ad8e13aa4365cec24ab24169b1abe93209263e4cfea4b52e0faccaf934182c84e8eb5dc49336c885358b4b66c48d38900f890fde5e

Patch0:     disable-extfs-test.patch

Requires: glib >= 2.58.3
Requires: pcre
Requires: slang

BuildRequires: glib-devel >= 2.58.3
BuildRequires: pcre-devel
BuildRequires: slang-devel

%description
MC (Midnight Commander) is a text-mode full-screen file manager and visual shell

%prep
%autosetup -p1

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
%if 0%{?with_check}
make %{?_smp_mflags} -k check
%endif

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_bindir}/*
%{_libexecdir}/*
%{_datadir}/*
%exclude %{_usrsrc}
%exclude %dir %{_libdir}/debug

%changelog
* Wed Nov 15 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.8.25-3
- Version bump due to glib change
* Sat Mar 26 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.8.25-2
- Exclude debug symbols properly
* Mon Dec 14 2020 Gerrit Photon <photon-checkins@vmware.com> 4.8.25-1
- Automatic Version Bump
* Thu Sep 06 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.8.21-1
- Update to version 4.8.21
* Fri Aug 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.8.19-2
- Disable extfs test
* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 4.8.19-1
- Update package version
* Tue Jul 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.8.17-1
- Initial build. First version
