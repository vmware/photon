Summary:	Netwide Assembler.
Name:		nasm
Version:	2.12.02
Release:	1%{?dist}
License:	BSD
URL:		http://www.nasm.us
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.nasm.us/pub/nasm/releasebuilds/%{version}/%{name}-%{version}.tar.gz
%define sha1 nasm=6d23d4be63f3a73d7df3053e65168f7906dd99e7
%description
NASM (Netwide Assembler) is an 80x86 assembler designed for portability and modularity. It includes a disassembler as well. 
%prep
%setup -q 
%build
./configure --prefix=%{_prefix}
make %{?_smp_mflags}
%install
make INSTALLROOT=%{buildroot} install
%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*
%changelog
*	Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 2.12.02-1
-	Initial version
