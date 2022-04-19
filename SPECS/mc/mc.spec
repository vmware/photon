Summary:        File manager
Name:           mc
Version:        4.8.28
Release:        1%{?dist}
License:        GPLv3+
URL:            https://www.midnight-commander.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://ftp.midnight-commander.orgtar/%{name}-%{version}.tar.xz
%define sha512  mc=ca3b3a57281e9387cb52bf1fcfc3f39a4d5f438aafc256dc492c192678824f67c983a852c759664efc5bc6d0de471c9b3929834f8301f6302ca1ebeee513fdfd
Requires:       glib pcre slang
BuildRequires:  glib-devel pcre-devel slang-devel

%description
MC (Midnight Commander) is a text-mode full-screen file manager and visual shell.

%prep
%autosetup

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install

%check
make %{?_smp_mflags} -k check

%files
%defattr(-,root,root)
/etc/*
/usr/bin/*
%exclude /usr/lib
/usr/libexec/*
/usr/share/*
%exclude /usr/src

%changelog
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 4.8.28-1
-   Automatic Version Bump
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 4.8.26-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 4.8.25-1
-   Automatic Version Bump
*   Thu Sep 06 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.8.21-1
-   Update to version 4.8.21
*   Fri Aug 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.8.19-2
-   Disable extfs test
*   Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 4.8.19-1
-   Update package version
*   Tue Jul 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.8.17-1
-   Initial build. First version.
