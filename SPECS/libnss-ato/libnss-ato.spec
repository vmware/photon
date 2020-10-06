%global commitversion 603cae8
Summary:        libnss-ato
Name:           libnss-ato
Version:        20201005
Release:        1%{?dist}
License:        GNU General Public License
URL:            https://github.com/donapieppo/libnss-ato
Source0:        %{name}-%{version}.tar.gz
%define sha1    libnss-ato=914a386b048f8caaa0b11a11fedf51df9f465de6
Group:	        Development/Tools
Vendor:	        VMware, Inc.
Distribution: 	Photon
Provides:       libnss_ato
Requires:       nss
BuildRequires:  nss-devel

%description
The libnss_ato module is a set of C library extensions,
which allows to map every nss request for unknown user to a single predefined user.

%prep
%setup -q -n %{name}-%{commitversion}

%build
make all %{?_smp_mflags} CFLAGS="%{optflags}" LDFLAGS=""

%install
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} install
mkdir %{buildroot}/lib
mv libnss_ato*so* %{buildroot}/lib/

%check
./libnss_ato_test root

%files
%defattr(-,root,root)
/lib/libnss_ato*
%exclude %{_mandir}/*

%changelog
* Mon Oct 05 2020 Gerrit Photon <photon-checkins@vmware.com> 20201005-1
- Automatic Version Bump
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.6-3
- Ensure non empty debuginfo
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.6-2
- GA - Bump release of all rpms
* Wed Oct 28 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging. First version
