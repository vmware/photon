Summary:       Fools programs into thinking they are running with root permission
Name:          fakeroot-ng
Version:       0.18
Release:       5%{?dist}
URL:           http://fakeroot-ng.lingnu.com
Group:         System Environment/Base
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: http://downloads.sourceforge.net/project/fakerootng/fakeroot-ng/%{version}/fakeroot-ng-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0:        Add-sched-h-to-process-cpp.patch

BuildArch:     x86_64

%description
Fakeroot-ng is a clean re-implementation of fakeroot. The core idea
is to run a program, but wrap all system calls that program performs
so that it thinks it is running as root, while it is, in practice,
running as an unprivileged user. When the program is trying to perform
a privileged operation (such as modifying a file's owner or creating
a block device), this operation is emulated, so that an unprivileged
operation is actually carried out, but the result of the privileged
operation is reported to the program whenever it attempts to query
the result.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%doc %{_mandir}/man1/%{name}.1.gz

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.18-5
- Release bump for SRP compliance
* Mon Sep 19 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 0.18-4
- Fix build with latest tool chain
* Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 0.18-3
- Adding BuildArch
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.18-2
- GA - Bump release of all rpms
* Fri Jul 10 2015 Luis Zuniga <lzuniga@vmware.com> 0.17-0.1
- Initial build for Photon
