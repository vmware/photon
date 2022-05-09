Summary:        Shell tool for executing jobs in parallel
Name:           parallel
Version:        20220622
Release:        1%{?dist}
License:        GPLv3+ and GFDL
Group:          Productivity/File utilities
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
Url:            https://www.gnu.org/software/parallel/
Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2
%define sha512  parallel=d01d86cd2ac373534d147eee8aa666fe26e7207362ea9c036c3744125f72c936d15cf2059429636454f21c8e8c6b3a60c8d761ddfde97ba7388d2cd00495bfa4
Requires:       perl
Requires:       gdbm

%description
GNU parallel is a shell tool for executing jobs concurrently locally or using remote computers.
A job is typically a single command or a small script that has to be run for each of the lines
in the input. The typical input is a list of files, a list of hosts, a list of users,
a list of URLs, or a list of tables.

%package        doc
Summary:        Documentation for parallel tool
Group:          Documentation
Requires:       parallel = %{version}-%{release}
%description    doc
It contains documentation for parallel shell tool

%prep
%autosetup

%build
%configure
%make_build %{?_smp_mflags}

%install
cd src/
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%check
%if 0%{?with_check}
%make_build %{?_smp_mflags} check
%endif

%files
%defattr(-,root,root)
%license LICENSES/GPL-3.0-or-later.txt LICENSES/CC-BY-SA-4.0.txt LICENSES/GFDL-1.3-or-later.txt
%doc README NEWS
%{_bindir}/parallel
%{_bindir}/parcat
%{_bindir}/parset
%{_bindir}/parsort
%{_bindir}/env_parallel*
%{_bindir}/sem
%{_bindir}/sql
%{_bindir}/niceload

%files doc
%defattr(-,root,root)
%{_docdir}/*
%{_mandir}/man1/*
%{_mandir}/man7/*

%changelog
* Mon Apr 04 2022 Prashant S Chauhan <psinghchauha@vmware.com> 20220622-1
- parallel initial build
