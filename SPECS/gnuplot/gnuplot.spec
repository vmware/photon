Summary:        Gnuplot is a portable command-line driven graphing utility.
Name:           gnuplot
Version:        5.2.4
Release:        1%{?dist}
License:        Freeware
URL:            http://www.gnuplot.info/
Group:          Applications
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%define sha1    gnuplot=e31e8d9875216f65f9ed0e57b2f62d9dfb0f0714

%description
Gnuplot is a portable command-line driven graphing utility for Linux, OS/2, MS Windows, OSX, VMS, and many other platforms. The source code is copyrighted but freely distributed (i.e., you don't have to pay for it). It was originally created to allow scientists and students to visualize mathematical functions and data interactively, but has grown to support many non-interactive uses such as web scripting. It is also used as a plotting engine by third-party applications like Octave. Gnuplot has been supported and under active development since 1986.

%prep
%setup -q

%build
./configure --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --disable-static \
    --enable-shared
make

%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*


%changelog
*   Thu Sep 06 2018 Anish Swaminathan <anishs@vmware.com> 5.2.4-1
-   Update version to 5.2.4
*   Wed Apr 12 2017 Danut Moraru <dmoraru@vmware.com> 5.0.6-1
-   Update version to 5.0.6
*   Tue Nov 29 2016 Xiaolin Li <xiaolinl@vmware.com> 5.0.5-1
-   Add gnuplot 5.0.5 package.


