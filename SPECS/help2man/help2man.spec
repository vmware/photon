Name:       help2man
Summary:    Create simple man pages from --help output
Version:    1.48.5
Release:    4%{?dist}
URL:        https://www.gnu.org/software/help2man
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon

Source:         https://ftp.gnu.org/gnu/help2man/%{name}-%{version}.tar.xz
%define sha512 %{name}=800eb0daa9daef8e423d52ede55eee2960122ea0269865295afada4cf4fcc1c6791da8429c3a57c0fc1bf0a14c8a77953952325413a8faa5dd07b1bc5bc0edd1

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl

BuildArch:      noarch

%description
help2man is a script to create simple man pages from the --help and
--version output of programs.

Since most GNU documentation is now in info format, this provides a
way to generate a placeholder man page pointing to that resource while
still providing some useful information.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%configure
%make_build %{?_smp_mflags}

%install
make install_l10n DESTDIR=%{buildroot} %{?_smp_mflags}
%{make_install} %{?_smp_mflags}

%find_lang %name --with-man

%files -f %name.lang
%defattr(-,root,root)
%doc README NEWS THANKS
%license COPYING
%{_bindir}/help2man
%{_infodir}/*
%{_mandir}/man1/*

%changelog
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.48.5-4
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.48.5-3
- Release bump for SRP compliance
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 1.48.5-2
- Rebuild for perl version upgrade to 5.36.0
* Fri Dec 10 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.48.5-1
- Intial version. Needed for rpm-4.17.0
