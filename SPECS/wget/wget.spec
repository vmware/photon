Summary:	A network utility to retrieve files from the Web
Name:		wget
Version:	1.15
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/wget/wget.html
Group:		System Environment/NetworkingPrograms
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
%define sha1 wget=e9fb1d25fa04f9c69e74e656a3174dca02700ba1
Patch0:		cve-2014-4877.patch
Requires:	openssl
BuildRequires:	openssl-devel
%description
The Wget package contains a utility useful for non-interactive 
downloading of files from the Web.
%prep
%setup -q
%patch0 -p1

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
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.15-1
-	Initial build.	First version
