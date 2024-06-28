Summary:      Improved WHOIS client
Name:         whois
Version:      5.5.15
Release:      2%{?dist}
License:      GPLv2+
URL:          https://github.com/rfc1036/whois
Group:        Productivity/Networking/Other
Vendor:       VMware, Inc.
Distribution: Photon

Source0: https://ftp.debian.org/debian/pool/main/w/%{name}/%{name}_%{version}.tar.xz
%define sha512 %{name}=e173927fd3428d27bc8ab34b1a66b82d6a2cfc107245755868bdd33cb7eb1b8159e87774c3a751d9694e65b3d870b9904dc9a3c657dca385950c8a19be1fa61c

BuildRequires:  pkg-config
BuildRequires:  xz-devel
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  openssl-devel

%description
Searches for an object in a RFC 3912 database.

This version of the WHOIS client tries to guess the right server to ask for
the specified object. If no guess can be made it will connect to
whois.networksolutions.com for NIC handles or whois.arin.net for IPv4
addresses and network names.

%package nls
Summary:    Gettext catalogs for whois tools
BuildArch:  noarch

%description nls
whois tools messages translated into different natural languages.

%package -n mkpasswd
Summary:   Encrypt a password with crypt(3) function using a salt
Requires:  openssl
Conflicts: expect

%description -n mkpasswd
mkpasswd tool encrypts a given password with the crypt(3) libc function
using a given salt.

%prep
%autosetup -p1 -n %{name}

%build
%make_build HAVE_LIBIDN2=1 \
            HAVE_ICONV=1 \
            HAVE_CRYPT_GENSALT=1

%install
%make_install %{?_smp_mflags}

%find_lang %{name}

%files
%defattr(-,root,root)
%{_bindir}/whois
%{_mandir}/man1/%{name}.*
%{_mandir}/man5/%{name}.*

%files nls -f %{name}.lang
%defattr(-,root,root)

%files -n mkpasswd
%defattr(-,root,root)
%{_bindir}/mkpasswd
%{_mandir}/man1/mkpasswd.*

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.5.15-2
- Bump version as a part of openssl upgrade
* Tue Feb 14 2023 Nitesh Kumar <kunitesh@vmware.com> 5.5.15-1
- Initial version, needed by fail2ban.
