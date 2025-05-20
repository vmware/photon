Summary:        Programmable completion for Bash
Name:           bash-completion
Version:        2.15.0
Release:        1%{?dist}
URL:            https://github.com/scop/bash-completion
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/scop/bash-completion/releases/download/%{version}/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildArch: noarch

BuildRequires: automake
BuildRequires: make

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-pexpect
%endif

Requires: bash

Conflicts: bash < 5.2-8

%description
%{name} is a collection of shell functions that take advantage
of the programmable completion feature of bash.

%package devel
Summary: Development files for %{name}
Requires: %{name} =  %{version}-%{release}

%description devel
This package contains development files for %{name}.

%prep
%autosetup -p1

%build
autoreconf -vif
%configure
%make_build

%install
%make_install %{?_smp_mflags}

rm %{buildroot}%{_datadir}/%{name}/completions/{cowsay,cowthink} \
   %{buildroot}%{_datadir}/%{name}/completions/makepkg \
   %{buildroot}%{_datadir}/%{name}/completions/prelink \
   %{buildroot}%{_datadir}/%{name}/completions/javaws

%if 0%{?with_check}
%check
%make_build check
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/profile.d/bash_completion.sh
%{_sysconfdir}/bash_completion.d/000_bash_completion_compat.bash
%{_datadir}/%{name}/

%files devel
%defattr(-,root,root)
%{_datadir}/cmake/
%{_datadir}/pkgconfig/%{name}.pc

%changelog
* Fri May 09 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.15.0-1
- Initial version.
