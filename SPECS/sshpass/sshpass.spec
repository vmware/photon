Summary:	Noninteractive ssh password provider 
Name:		sshpass
Version:	1.05
Release:	1%{?dist}
License:	GPLv2+
URL:		http://sourceforge.net/projects/sshpass/
Source0:	http://downloads.sourceforge.net/project/sshpass/sshpass/1.05/sshpass-1.05.tar.gz
%define sha1 sshpass=6dafec86dd74315913417829542f4023545c8fd7
Group:		Applications/Networking
Vendor:		VMware, Inc.
Distribution:	Photon
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
echo '*** sshpass check is probably not supported by source, the test-suite will NOT run ***'

%clean 
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS
%{_bindir}
%{_mandir}/man1

%changelog
*	Fri Sep 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.05-1
-	Initial version
