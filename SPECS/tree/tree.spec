Summary:        Recursive directory listing command.
Name:           tree
Version:        1.7.0
Release:        1%{?dist}
License:        GPLv2+
URL:            http://mama.indstate.edu/users/ice/tree/
Group:          Applications
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://mama.indstate.edu/users/ice/tree/src/tree-%{version}.tgz
%define sha1    tree=35bd212606e6c5d60f4d5062f4a59bb7b7b25949

%description
Tree is a recursive directory listing command that produces a depth indented listing of files, which is colorized ala dircolors if the LS_COLORS environment variable is set and output is to tty. Tree has been ported and reported to work under the following operating systems: Linux, FreeBSD, OS X, Solaris, HP/UX, Cygwin, HP Nonstop and OS/2.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install BINDIR=%{buildroot}%{_bindir} \
             MANDIR=%{buildroot}%{_mandir}/man1

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%changelog
*   Thu Dec 01 2016 Xiaolin Li <xiaolinl@vmware.com> 1.7.0-1
-   Add tree package.


