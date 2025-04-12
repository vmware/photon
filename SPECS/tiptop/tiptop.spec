Summary:    Display hardware performance counters for Linux tasks
Name:       tiptop
Version:    2.3.2
Release:    1%{?dist}
License:    GPLv2
URL:        https://team.inria.fr/pacap/software/tiptop
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:  Photon

Source0: https://files.inria.fr/pacap/tiptop/%{name}-%{version}.tar.gz
%define sha512 %{name}=98d69edbf7bcdee6bbf6dd2b21f1429b6417767187a8fb1553ba45659705815010362fb091e4166beab247439ee227df5feab5c49c8194ed9a7d29003b0c1ff0

BuildRequires: bison

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
%autosetup -p1

%build
%configure
# make doesn't support _smp_mflags
make -j1

%install
install -D src/tiptop %{buildroot}%{_bindir}/tiptop
install -D src/ptiptop %{buildroot}%{_bindir}/ptiptop

%files
%defattr(-,root,root)
%{_bindir}/*

%changelog
* Sat Apr 12 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.3.2-1
- Upgrade to v2.3.2
- Cleanup spec
* Wed Sep 28 2022 Bo Gan <ganb@vmware.com> 2.3.1-2
- Use correct configure options.
* Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 2.3.1-1
- Update version to 2.3.1.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3-2
- GA - Bump release of all rpms
* Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 2.3-1
- Initial build. First version
