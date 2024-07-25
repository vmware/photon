Summary:        Programmable completion for Bash
Name:           bash-completion
Version:        2.11
Release:        1%{?dist}
License:        GPL-2.0-or-later
URL:            https://github.com/scop/bash-completion
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/scop/bash-completion/releases/download/%{version}/%{name}-%{version}.tar.xz
%define sha512 %{name}=41585f730b5114d397831ba36d10d05643c6a6179e746ddc49aa1cbef61ea5525fd2f09b2e474adee14e647f99df8d5983ee48e29a59d8a30e1daf7fb1837e06

BuildArch: noarch

BuildRequires: automake
BuildRequires: make

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-pexpect
%endif

Requires: bash

Conflicts: bash < 5.2-2

%description
%{name} is a collection of shell functions that take advantage
of the programmable completion feature of bash.

%prep
%autosetup -p1

%build
autoreconf -fi -v
%configure
%make_build

%install
%make_install %{?_smp_mflags}

rm %{buildroot}%{_datadir}/%{name}/completions/{cowsay,cowthink} \
   %{buildroot}%{_datadir}/%{name}/completions/makepkg \
   %{buildroot}%{_datadir}/%{name}/completions/prelink

%if 0%{?with_check}
%check
make check %{?_smp_mflags}
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/profile.d/bash_completion.sh
%{_datadir}/%{name}/
%{_datadir}/cmake/
%{_datadir}/pkgconfig/%{name}.pc

%changelog
* Sun May 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.11-1
- Initial version.
