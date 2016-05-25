Summary:	A network utility to retrieve files from the Web
Name:		wget
Version:	1.17.1
Release:	2%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/wget/wget.html
Group:		System Environment/NetworkingPrograms
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
%define sha1 wget=8ae737ab2252607ce708f98d1dd7559ebf047f48
Requires:	openssl
BuildRequires:	openssl-devel
%description
The Wget package contains a utility useful for non-interactive 
downloading of files from the Web.
%prep
%setup -q

%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--disable-silent-rules \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--sysconfdir=/etc \
	--with-ssl=openssl 
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/etc
cat >> %{buildroot}/etc/wgetrc <<-EOF
#	default root certs location
	ca_certificate=/etc/pki/tls/certs/ca-bundle.crt
EOF
rm -rf %{buildroot}/%{_infodir}
%find_lang %{name}
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%clean
rm -rf %{buildroot}/*
%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) /etc/wgetrc
%{_bindir}/*
%{_mandir}/man1/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	1.17.1-2
-	GA - Bump release of all rpms
*	Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.17.1-1
-	Upgrade version
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.15-1
-	Initial build.	First version
