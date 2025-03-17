Summary: Tools to read/write MSR (Model Specific Registers)
Name:    msr-tools
Version: 1.3
Release: 3%{?dist}
URL: https://01.org/msr-tools/downloads
Source0: %{name}-%{version}.zip
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:  Photon

Source1: license.txt
%include %{SOURCE1}

BuildRequires: unzip

%description
MSR Tools project provides utilities to access the processor MSRs and CPU ID directly.
This project is composed of three different user space console applications.
rdmsr – read MSR from any CPU or all CPUs
wrmsr – write values to MSR on any CPU or all CPUs
cpuid – show identification and feature information of any CPU

%prep
%autosetup -p1 -n msr-tools-master

%build
make %{?_smp_mflags}

%install
install -D rdmsr %{buildroot}%{_sbindir}/rdmsr
install -D wrmsr %{buildroot}%{_sbindir}/wrmsr
install -D cpuid %{buildroot}%{_sbindir}/msr-cpuid

%files
%defattr(-,root,root)
%{_sbindir}/*

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.3-3
- Release bump for SRP compliance
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.3-2
- GA - Bump release of all rpms
* Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 2.3-1
- Initial build. First version
