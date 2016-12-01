Summary:        Gnuplot is a portable command-line driven graphing utility.
Name:           gnuplot
Version:        5.0.5
Release:        1%{?dist}
License:        Freeware
URL:            http://www.gnuplot.info/
Group:          Applications
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://downloads.sourceforge.net/gnuplot/gnuplot-5.0.5.tar.gz
%define sha1    gnuplot=c35f55657fdc33217dd70bbf3148578563ecaad1

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
*   Tue Nov 29 2016 Xiaolin Li <xiaolinl@vmware.com> 5.0.5-1
-   Add gnuplot 5.0.5 package.


