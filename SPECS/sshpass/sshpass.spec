Summary:	Noninteractive ssh password provider 
Name:		sshpass
Version:	1.05
Release:	3%{?dist}
License:	GPLv2+
URL:		http://sourceforge.net/projects/sshpass/
Source0:	http://downloads.sourceforge.net/project/sshpass/sshpass/1.05/sshpass-1.05.tar.gz
%define sha1 sshpass=6dafec86dd74315913417829542f4023545c8fd7
Group:		Applications/Networking
Vendor:		VMware, Inc.
Distribution:	Photon
Requires:       openssh
%description
sshpass is a utility designed for running ssh using the mode referred to as "keyboard-interactive" password authentication, but in non-interactive mode. 
%prep
%setup -q
%build
./configure --prefix=%{_prefix} 
make %{?_smp_mflags}
%install
rm -rf %{buildroot}
make prefix=%{_prefix}	DESTDIR=%{buildroot} install

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%clean 
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS
%{_bindir}
%{_mandir}/man1

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.05-3
-	GA - Bump release of all rpms
*	Thu Apr 28 2016 Anish Swaminathan <anishs@vmware.com> 1.05-2
-	Add requires for openssh
*	Fri Sep 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.05-1
-	Initial version
