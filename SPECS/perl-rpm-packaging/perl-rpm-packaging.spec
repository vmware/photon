%global build_if %{photon_subrelease} >= 92

%global debug_package %{nil}

%define rpmhome %{_libdir}/rpm

Summary:        Tools for packaging Perl projects with rpm
Name:           perl-rpm-packaging
Version:        1.3
Release:        3%{?dist}
Group:          Development/Libraries
URL:            https://github.com/rpm-software-management/perl-rpm-packaging
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/rpm-software-management/perl-rpm-packaging/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  perl

Requires:       perl

Conflicts: rpm-build < 6.0.1

%description
This package contains the RPM scripts for "Provides" and "Requires" detection of perl packages.

%prep
%autosetup -p1

%build

%install
mkdir -p %{buildroot}%{rpmhome}
cp -r fileattrs %{buildroot}%{rpmhome}
cp scripts/perl.* %{buildroot}%{rpmhome}

chmod 755 %{buildroot}%{rpmhome}/perl.* \
          %{buildroot}%{rpmhome}/fileattrs/perl*

%files
%defattr(-,root,root)
%{rpmhome}/*

%changelog
* Wed Apr 01 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.3-3
- Conflict with earlier versions of rpm-build
* Tue Mar 31 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.3-2
- Disable debug info package
* Sun Mar 29 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.3-1
- Initial version, needed by rpm-6.x
