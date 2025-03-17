#need to deactivate debuginfo since debugfiles.list is empty
%define debug_package %{nil}

Summary:        Recursive directory listing command.
Name:           tree
Version:        2.0.4
Release:        2%{?dist}
URL:            http://mama.indstate.edu/users/ice/tree/
Group:          Applications
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://mama.indstate.edu/users/ice/tree/src/tree-%{version}.tgz

Source1: license.txt
%include %{SOURCE1}

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
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 2.0.4-2
- Release bump for SRP compliance
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.4-1
- Automatic Version Bump
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.2-1
- Automatic Version Bump
* Wed Jul 15 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.0-1
- Automatic Version Bump
* Thu Dec 01 2016 Xiaolin Li <xiaolinl@vmware.com> 1.7.0-1
- Add tree package.
