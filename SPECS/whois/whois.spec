Summary:      Improved WHOIS client
Name:         whois
Version:      5.5.15
Release:      2%{?dist}
URL:          https://github.com/rfc1036/whois
Group:        Productivity/Networking/Other
Vendor:       VMware, Inc.
Distribution: Photon

Source0: https://ftp.debian.org/debian/pool/main/w/%{name}/%{name}_%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 5.5.15-2
- Release bump for SRP compliance
* Tue Feb 14 2023 Nitesh Kumar <kunitesh@vmware.com> 5.5.15-1
- Initial version, needed by fail2ban.
