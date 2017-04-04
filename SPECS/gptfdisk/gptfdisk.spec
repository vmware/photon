Summary:	gptfdisk-1.0.1
Name:		gptfdisk
Version:	1.0.1
Release:	3%{?dist}
License:	GPLv2+
URL:		http://sourceforge.net/projects/gptfdisk/
Group:		System Environment/Filesystem and Disk management
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://downloads.sourceforge.net/project/gptfdisk/gptfdisk/1.0.1/gptfdisk-1.0.1.tar.gz
%define sha1 gptfdisk=ad28c511c642235815b83fffddf728c117057cba
Patch0:	        gptfdisk-1.0.1-convenience-1.patch	
Requires: 	popt >= 1.16
BuildRequires:	popt-devel
BuildRequires:	ncurses-devel >= 6.0-3
Requires:	ncurses >= 6.0-3
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
*   Mon Apr 3 2017 Alexey Makhalov <amakhalov@vmware.com> 1.0.1-3
-   Use specified version of ncurses wich has long chtype and mmask_t
    (see ncurses changelog)
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1-2
-   GA - Bump release of all rpms
*   Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 1.0.1-1
-   Updated Version.
*   Thu Oct 30 2014 Divya Thaluru <dthaluru@vmware.com> 0.8.10-1
-   Initial build.	First version
