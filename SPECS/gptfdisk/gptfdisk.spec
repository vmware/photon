Summary:	gptfdisk-0.8.10
Name:		gptfdisk
Version:	0.8.10 
Release:	1%{?dist}
License:	GPLv2+
URL:		http://sourceforge.net/projects/gptfdisk/
Group:		System Environment/Filesystem and Disk management
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://downloads.sourceforge.net/project/gptfdisk/gptfdisk/0.8.10/gptfdisk-0.8.10.tar.gz
%define sha1 gptfdisk=1708e232220236b6bdf299b315e9bc2205c01ba5
Patch0:		http://www.linuxfromscratch.org/patches/blfs/systemd/gptfdisk-0.8.10-convenience-1.patch
Requires: 	popt >= 1.16
BuildRequires:	popt-devel
BuildRequires:	ncurses-devel
Requires:	ncurses
%description
The gptfdisk package is a set of programs for creation and maintenance of GUID Partition 
Table (GPT) disk drives. A GPT partitioned disk is required for drives greater than 2 TB 
and is a modern replacement for legacy PC-BIOS partitioned disk drives that use a 
Master Boot Record (MBR). The main program, gdisk, has an inteface similar to the 
classic fdisk program. 
%prep
%setup -q
%patch0 -p1
%build
make %{?_smp_mflags} POPT=1
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install POPT=1
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/sbin/*
%{_mandir}/man8/*
%changelog
*	Thu Oct 30 2014 Divya Thaluru <dthaluru@vmware.com> 0.8.10-1
-	Initial build.	First version
