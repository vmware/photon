Summary: Display hardware performance counters for Linux tasks
Name:    tiptop
Version: 2.3.1
Release: 1%{?dist}
License: GPLv2
URL: http://tiptop.gforge.inria.fr/
Source: %{name}-%{version}.tar.gz
%define sha1 tiptop=52ccd0d5dfa0a8a6f692c379e560a394a6f376b9
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:  Photon

%description
Hardware performance monitoring counters have recently received a lot of attention.
They have been used by diverse communities to understand and improve the quality of computing systems:
for example,architects use them to extract application characteristics and propose new hardware mechanisms;
compiler writers study how generated code behaves on particular hardware;
software developers identify critical regions of their applications and evaluate design choices to select the best performing implementation.
We propose that counters be used by all categories of users, in particular non-experts, and we advocate that a few simple metrics derived from these counters are relevant and useful.
For example, a low IPC (number of executed instructions per cycle) indicates that the hardware is not performing at its best; a high cache miss ratio can suggest several causes,
such as conflicts between processes in a multicore environment.

%prep
%setup -q

%build
./configure
make
%install
install -D  src/tiptop %{buildroot}%{_bindir}/tiptop
install -D  src/ptiptop %{buildroot}%{_bindir}/ptiptop

%files
%defattr(-,root,root)
%{_bindir}/*

%changelog
*       Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 2.3.1-1
-       Update version to 2.3.1.
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3-2
-	GA - Bump release of all rpms
*	Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 2.3-1
-   Initial build.  First version
