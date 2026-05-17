%global build_if %{photon_subrelease} >= 91

%define srcname         wal2json
%define main_version    2_6
%global pgmajorversion  18
%global _pgbaseinstdir  %{_usr}/pgsql/%{pgmajorversion}
%global _pglibdir       %{_pgbaseinstdir}/lib/postgresql

Summary:        JSON output plugin for changeset extraction
Name:           wal2json18
Version:        2.6
Release:        2%{?dist}
URL:            https://github.com/eulerto/wal2json
Group:          Productivity/Databases/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/eulerto/wal2json/archive/refs/tags/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: postgresql%{pgmajorversion}-devel

Requires: postgresql%{pgmajorversion}-libs

%description
wal2json is an output plugin for logical decoding.
It means that the plugin have access to tuples produced by INSERT and UPDATE.
Also, UPDATE/DELETE old row versions can be accessed depending on the configured replica identity.

%prep
%autosetup -n %{srcname}-%{srcname}_%{main_version}

%build
%{make_build}

%install
%{make_install}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%dir %{_pgbaseinstdir}
%dir %{_pgbaseinstdir}/lib
%dir %{_pglibdir}
%dir %{_pglibdir}/bitcode
%dir %{_pglibdir}/bitcode/%{srcname}
%{_pglibdir}/%{srcname}.so
%{_pglibdir}/bitcode/%{srcname}.index.bc
%{_pglibdir}/bitcode/%{srcname}/%{srcname}.bc

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.6-2
- Extended to build for subrelease 91 and above
* Mon Mar 02 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.6-1
- Initial build
