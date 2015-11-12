Summary:	libnss-ato
Name:		libnss-ato
Version:	2.3.6
Release:	1%{?dist}
License:	GNU General Public License
URL:		https://github.com/donapieppo/libnss-ato
Source0:	%{name}-%{version}.tar.gz
Patch0:     destdir.patch
%define sha1 libnss-ato=7a3ec992cc443ac0e34ff2de43dee91b0bdf3f06
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
Provides:	libnss_ato
Requires:   nss
BuildRequires: nss-devel

%description
The libnss_ato module is a set of C library extensions which allows to map every nss request for unknown user to a single predefined user.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%build
make
%install
make DESTDIR=%{buildroot} install
%files
%defattr(-,root,root)
/lib/libnss_ato*
%exclude %{_mandir}/*

%changelog
*	Wed Oct 28 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-	Initial packaging. First version
