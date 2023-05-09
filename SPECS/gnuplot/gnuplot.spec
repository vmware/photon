Summary:        Gnuplot is a portable command-line driven graphing utility.
Name:           gnuplot
Version:        5.4.6
Release:        1%{?dist}
License:        Freeware
URL:            http://www.gnuplot.info/
Group:          Applications
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%define sha512  %{name}=a78333f7c0ed3429b24fcdeb6296e67fb760e6f8ffc0801a6b379fcb12ae7e80cebe65a2655cb3530c2a2d4083adc34060c9a7cbe67ce98b660682c0edba174b

%description
Gnuplot is a portable command-line driven graphing utility for Linux, OS/2, MS Windows, OSX, VMS, and many other platforms. The source code is copyrighted but freely distributed (i.e., you don't have to pay for it). It was originally created to allow scientists and students to visualize mathematical functions and data interactively, but has grown to support many non-interactive uses such as web scripting. It is also used as a plotting engine by third-party applications like Octave. Gnuplot has been supported and under active development since 1986.

%prep
%autosetup -p1

%build
%configure \
    --disable-static \
    --enable-shared
make %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*

%changelog
*   Tue May 09 2023 Shivani Agarwal <shivania2@vmware.com> 5.4.6-1
-   Upgrade to 5.4.6 and fix CVE-2020-25412, CVE-2020-25559
*   Sun Nov 25 2018 Ashwin H <ashwinh@vmware.com> 5.2.4-2
-   Fix %check
*   Thu Sep 06 2018 Anish Swaminathan <anishs@vmware.com> 5.2.4-1
-   Update version to 5.2.4
*   Wed Apr 12 2017 Danut Moraru <dmoraru@vmware.com> 5.0.6-1
-   Update version to 5.0.6
*   Tue Nov 29 2016 Xiaolin Li <xiaolinl@vmware.com> 5.0.5-1
-   Add gnuplot 5.0.5 package.
