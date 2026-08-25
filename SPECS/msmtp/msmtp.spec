%global build_if %{photon_subrelease} >= 91

Name:           msmtp
Version:        1.8.32
Release:        4%{?dist}
Summary:        Provides msmtp client and server
URL:            https://marlam.de/msmtp/
Group:          Email/Server/Library
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/marlam/msmtp/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  autoconf
BuildRequires:  texinfo
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gnutls-devel
BuildRequires:  jsoncpp
BuildRequires:  make

%description
This package provides minimal SMTP server (msmtpd) and SMTP client (msmtp).

%package doc
Summary: msmtp docs package
%description doc
Provides documents for the msmtp package

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}
rm -f ChangeLog.old

%build
autoreconf -ivf
%configure --with-tls=gnutls --disable-rpath --with-msmtpd
%make_build

%install
%make_install
%find_lang %{name}
rm -rf scripts/Makefile* scripts/emacs scripts/set_sendmail scripts/vim %{buildroot}%{_infodir}
install -d %{buildroot}%{_datadir}/%{name}
cp -r scripts/msmtpq scripts/msmtpqueue %{buildroot}%{_datadir}/%{name}

%files -f %{name}.lang
%license COPYING
%doc AUTHORS NEWS README THANKS
%{_bindir}/%{name}*
%{_datadir}/%{name}

%files doc
%{_mandir}/man1/%{name}*.1*
%doc doc/msmtprc-system.example doc/msmtprc-user.example

%changelog
* Fri Jun 05 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.8.32-4
- Add texinfo to BuildRequires
* Sat May 16 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.8.32-3
- Extended to build for subrelease 91 and above
* Tue May 05 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 1.8.32-2
- Version bump due to gnutls update
* Wed Mar 25 2026 Dweep Advani <dweep.advani@broadcom.com> 1.8.32-1
- Add msmtp package
