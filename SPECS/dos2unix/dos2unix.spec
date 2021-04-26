Name:           dos2unix
Version:        7.4.2
Release:        1%{?dist}
License:        BSD
Summary:        Text file format converters
URL:            https://waterlan.home.xs4all.nl/dos2unix.html
Source0:        https://waterlan.home.xs4all.nl/dos2unix/%{name}-%{version}.tar.gz
%define sha1    %{name}=e2d6dab6a57e122de330d36639ccb43a6432534d
Vendor:         VMware, Inc
Distribution:   Photon
Group:          System/Tools

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  make

Provides:       unix2dos

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
make test

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
* Mon Apr 26 2021 Shreenidhi Shedi <sshedi@vmware.com> 7.4.2-1
- Initial version
