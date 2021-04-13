Summary:        Gnuplot is a portable command-line driven graphing utility.
Name:           gnuplot
Version:        5.4.1
Release:        1%{?dist}
License:        Freeware
URL:            http://www.gnuplot.info/
Group:          Applications
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%define sha1    gnuplot=bb1cd34f8ec0357eccef70122f0fd531ced5dd29

%description
Gnuplot is a portable command-line driven graphing utility for Linux, OS/2, MS Windows, OSX, VMS, and many other platforms. The source code is copyrighted but freely distributed (i.e., you don't have to pay for it). It was originally created to allow scientists and students to visualize mathematical functions and data interactively, but has grown to support many non-interactive uses such as web scripting. It is also used as a plotting engine by third-party applications like Octave. Gnuplot has been supported and under active development since 1986.

%prep
%setup -q

%build
%configure \
    --disable-static \
    --enable-shared
make

%check
make check

%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*


%changelog
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 5.4.1-1
-   Automatic Version Bump
*   Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 5.4.0-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 5.2.8-1
-   Automatic Version Bump
*   Sun Nov 25 2018 Ashwin H <ashwinh@vmware.com> 5.2.4-2
-   Fix %check
*   Thu Sep 06 2018 Anish Swaminathan <anishs@vmware.com> 5.2.4-1
-   Update version to 5.2.4
*   Wed Apr 12 2017 Danut Moraru <dmoraru@vmware.com> 5.0.6-1
-   Update version to 5.0.6
*   Tue Nov 29 2016 Xiaolin Li <xiaolinl@vmware.com> 5.0.5-1
-   Add gnuplot 5.0.5 package.


