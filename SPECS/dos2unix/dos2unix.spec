Name:           dos2unix
Version:        7.4.3
Release:        3%{?dist}
Summary:        Text file format converters
URL:            https://waterlan.home.xs4all.nl/dos2unix.html
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System/Tools

Source0:        https://waterlan.home.xs4all.nl/dos2unix/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  make

Provides:       unix2dos

Conflicts:      toybox < 0.8.6-1

%description
Convert text files with DOS or Mac line endings to Unix line endings and
vice versa.

%prep
%autosetup -p1

%build
%make_build

%install
%make_install
rm -rf %{buildroot}%{_docdir}
%find_lang %{name} --with-man --all-name

%check
make test %{?_smp_mflags}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%license COPYING.txt
%doc man/man1/dos2unix.htm ChangeLog.txt
%doc NEWS.txt README.txt TODO.txt
%{_bindir}/dos2unix
%{_bindir}/mac2unix
%{_bindir}/unix2dos
%{_bindir}/unix2mac
%{_mandir}/man1/*.1*

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 7.4.3-3
- Release bump for SRP compliance
* Sat Jan 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 7.4.3-2
- Bump version as a part of gettext upgrade
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 7.4.3-1
- Automatic Version Bump
* Tue Dec 07 2021 Shreenidhi Shedi <sshedi@vmware.com> 7.4.2-2
- Conflict with toybox < 0.8.6-1
* Mon Apr 26 2021 Shreenidhi Shedi <sshedi@vmware.com> 7.4.2-1
- Initial version
