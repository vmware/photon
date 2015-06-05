Summary:	Programs for searching through files
Name:		grep
Version:	2.21
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/grep
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://ftp.gnu.org/gnu/grep/%{name}-%{version}.tar.xz
Patch0:     out-of-bound-heap-read-CVE-2015-1345.patch
%description
The Grep package contains programs for searching through files.
%prep
%setup -q
%patch0 -p1
%build
./configure \
	--prefix=%{_prefix} \
	--bindir=/bin \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files -f %{name}.lang
%defattr(-,root,root)
/bin/*
%{_mandir}/*/*
%changelog
*   Mon Apr 6 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.21-1
-   Upgrading grep to 2.21 version, and adding 
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.16-1
-	Initial build. First version
