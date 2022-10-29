#need to deactivate debuginfo since debugfiles.list is empty
%define debug_package %{nil}

Summary:        Recursive directory listing command.
Name:           tree
Version:        2.0.4
Release:        1%{?dist}
License:        GPLv2+
URL:            http://mama.indstate.edu/users/ice/tree/
Group:          Applications
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://mama.indstate.edu/users/ice/tree/src/tree-%{version}.tgz
%define sha512  %{name}=9939c8f891f74576cff5afb27975ac40c402c07182a110a1d28d2e1e9bf93ce8da27fbc593d0aaee45eb68878c52f625154e728b12fd76c8b2c82431c803e861

%description
Tree is a recursive directory listing command that produces a depth indented listing of files, which is colorized ala dircolors if the LS_COLORS environment variable is set and output is to tty. Tree has been ported and reported to work under the following operating systems: Linux, FreeBSD, OS X, Solaris, HP/UX, Cygwin, HP Nonstop and OS/2.

%prep
%autosetup

%build
make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make install PREFIX=%{buildroot}/usr \
             MANDIR=%{buildroot}%{_mandir}/man1 \
             %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.4-1
- Automatic Version Bump
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.2-1
- Automatic Version Bump
* Wed Jul 15 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.0-1
- Automatic Version Bump
* Thu Dec 01 2016 Xiaolin Li <xiaolinl@vmware.com> 1.7.0-1
- Add tree package.
