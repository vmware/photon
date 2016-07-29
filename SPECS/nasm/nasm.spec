Summary:	Netwide Assembler.
Name:		nasm
Version:	2.11.08
Release:	1
License:	BSD
URL:		http://www.nasm.us
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.nasm.us/pub/nasm/releasebuilds/%{version}/%{name}-%{version}.tar.xz
%define sha1 nasm=6908296ac437b3ade79fadfaad0efcfd99582f70
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
*	Fri Jul 29 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.11.08-1
-	initial version
