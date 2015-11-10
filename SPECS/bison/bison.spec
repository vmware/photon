Summary:	Contains a parser generator
Name:		bison
Version:	3.0.2
Release:	3%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/bison
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/bison/%{name}-%{version}.tar.xz
%define sha1 bison=aeb1e3544007124009e5203afe86a5676580d444
BuildRequires:	m4
Requires:	m4
BuildRequires:	flex
Requires:	flex
%description
This package contains a parser generator
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}
%find_lang %{name} --all-name
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.a
%{_datarootdir}/%{name}/*
%{_datarootdir}/aclocal/*
%{_mandir}/*/*
%changelog
*	Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 3.0.2-3
-	Handled locale files with macro find_lang
*	Fri Jun 5 2015 Divya Thaluru <dthaluru@vmware.com> 3.0.2-2
-	Adding m4, flex package to build and run time required package 
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.0.2-1
-	Initial build. First version.
