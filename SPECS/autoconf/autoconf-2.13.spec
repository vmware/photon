Summary:	The package automatically configure source code
Name:		autoconf
Version:	2.13
Release:	3%{?dist}
License:	GPLv2
URL:		http://www.gnu.org/software/autoconf
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.gz
%define sha512 autoconf=602584f4c77b7a554aaa068eda5409b68eb0b3229e9c224bffb91c83c4314d25de15bd560a323626ff78f6df339c79e1ef8938c54b78ecadf4dc75c5241290ad
Patch0:         autoconf-2.13-consolidated_fixes-1.patch
BuildRequires:	m4 texinfo
Requires:	m4
Requires:       perl-Perl4-CoreLibs
BuildArch:      noarch
Obsoletes:      autoconf213 <= 2.13

%description
The package contains programs for producing shell scripts that can
automatically configure source code.

%prep
%autosetup -n autoconf-%{version} -p1
mv -v autoconf.texi autoconf213.texi
rm -v autoconf.info

%build
%configure --program-suffix=2.13
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
install -v -m644 autoconf213.info %{buildroot}/usr/share/info

%check
make -k check %{?_smp_mflags}  TESTSUITEFLAGS="1-500"

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/autoconf-%{version}/*
%{_datadir}/info

%changelog
*   Thu Nov 10 2022 Dweep Advani <amakhalov@vmware.com> 2.13-3
-   Rebuild for upgraded perl version 5.36.0
*   Thu Feb 11 2021 Alexey Makhalov <amakhalov@vmware.com> 2.13-2
-   Add explicit texinfo build dependency to avoid using preinstalled one.
*   Sat Oct 26 2019 Ankit Jain <ankitja@vmware.com> 2.13-1
-   Initial build.	First version
