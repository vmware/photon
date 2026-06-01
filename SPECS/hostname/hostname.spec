%global build_if %{photon_subrelease} >= 91

Summary:        Utility to set/show the host name or domain name
Name:           hostname
Version:        3.25
Release:        3%{?dist}
URL:            https://tracker.debian.org/pkg/hostname
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://deb.debian.org/debian/pool/main/h/hostname/hostname_%{version}.tar.xz

# debian doesn't include a copy of the license in their repo. It's legally required to be
# included with the distributed package.
Source1: gpl-2.0.txt

Source2: license.txt
%include %{SOURCE2}

Conflicts: net-tools

BuildRequires: gcc
BuildRequires: make

%description
hostname is a utility that can be used to maintain/manipulate the host name and the domain name. It
is also used to show the FQDN and the IP-Addresses.

%package docs
Summary: Hostname doc files

%description docs
Contains man page for hostname

%prep
%autosetup -p1 -n hostname

cp %{SOURCE1} .

%build
%make_build

%install
%make_install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYRIGHT
%license gpl-2.0.txt
%{_bindir}/*

%files docs
%{_mandir}/man1/*

%changelog
* Mon Jun 01 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 3.25-3
- Add conflicts for net-tools
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.25-2
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 3.25-1
- Initial packaging for Photon
