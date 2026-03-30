%global build_if %{photon_subrelease} >= 92

Name:           msmtp
Version:        1.8.32
Release:        1%{?dist}
Summary:        Provides msmtp client and server
URL:            https://marlam.de/msmtp/
Group:          Email/Server/Library
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/marlam/msmtp/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  autoconf
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
* Wed Mar 25 2026 Dweep Advani <dweep.advani@broadcom.com> 1.8.32-1
- Add msmtp package
