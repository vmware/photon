Summary:	The package automatically configure source code
Name:		autoconf213
Version:	2.13
Release:	1%{?dist}
License:	GPLv2
URL:		http://www.gnu.org/software/autoconf
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.gz
%define sha1 autoconf=e4826c8bd85325067818f19b2b2ad2b625da66fc
Patch0:         autoconf-2.13-consolidated_fixes-1.patch
BuildRequires:	m4
Requires:	m4
Requires:       perl-Perl4-CoreLibs
BuildArch:      noarch

%description
The package contains programs for producing shell scripts that can
automatically configure source code.

%prep
%setup -q -n autoconf-%{version}
%patch0 -p1
mv -v autoconf.texi autoconf213.texi
rm -v autoconf.info

%build
%configure --program-suffix=2.13
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -v -m644 autoconf213.info %{buildroot}/usr/share/info

%check
make -k check %{?_smp_mflags}  TESTSUITEFLAGS="1-500"

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/autoconf-%{version}/*
%{_datadir}/info

%changelog
*   Sat Oct 26 2019 Ankit Jain <ankitja@vmware.com> 2.13-1
-   Initial build.	First version
