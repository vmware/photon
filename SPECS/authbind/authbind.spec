%define debug_package %{nil}
Summary:	Operating system utility that allows programs to run as non-previleged user.
Name:		authbind
Version:	2.1.2
Release:	1%{?dist}
License:	GPL
URL:		http://www.gnu.org/software/grep
Group:		Applications/utils
Vendor:		VMware, Inc.
Distribution:   Photon
Source0:	http://ftp.debian.org/debian/pool/main/a/%{name}/%{name}-%{version}.tar.gz
%define sha1 authbind=18434ebfbff5560e8691ebafcb2896837447a98f
%description
The authbind software allows a program that would normally require superuser privileges to access privileged network services to run as a non-privileged user.

%prep
%setup -qn authbind
sed -i 's#-Wall#-Wall -Wno-unused-result#g' Makefile
sed 's#\/usr\/local#%{_prefix}#g' Makefile
%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_mandir}/man8
make install DESTDIR=%{buildroot}
make install_man DESTDIR=%{buildroot}
install -vsm 755 authbind %{buildroot}%{_bindir}
install -vsm 755 helper %{buildroot}%{_libdir}
install -vsm 755 libauthbind.so.1.0 %{buildroot}%{_libdir}
cp -r %{_sysconfdir}/%{name} %{buildroot}%{_sysconfdir}
cp authbind.1* %{buildroot}%{_mandir}/man1
cp authbind-helper.8* %{buildroot}%{_mandir}/man8

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_libdir}
%{_sysconfdir}/authbind
%{_mandir}
%changelog
*    Fri Jul 14 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.1.2-1
-    Initial build. First version
