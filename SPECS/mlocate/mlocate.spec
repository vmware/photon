Name:           mlocate
Version:        0.26
Release:        5%{?dist}
Summary:        An utility for finding files by name.
URL:            https://pagure.io/mlocate
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Applications/File

Source0: http://releases.pagure.org/mlocate/%{name}-%{version}.tar.xz

Source1: %{name}.sysusers

Source2: license.txt
%include %{SOURCE2}

BuildRequires:  sed
BuildRequires:  grep
BuildRequires:  xz
BuildRequires:  gettext
BuildRequires:  systemd-devel

%description
mlocate is a locate/updatedb implementation.  The 'm' stands for "merging":
updatedb reuses the existing database to avoid rereading most of the file
system, which makes updatedb faster and does not trash the system caches as
much.

%prep
%autosetup -p1

%build
%configure \
    --enable-nls \
    --disable-rpath

%make_build

%install
%make_install %{?_smp_mflags}
mv %{buildroot}%{_bindir}/locate %{buildroot}%{_bindir}/%{name}
mv %{buildroot}%{_bindir}/updatedb %{buildroot}%{_bindir}/updatedb.%{name}
mv %{buildroot}%{_mandir}/man1/locate.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%check
%make_build check

%clean
rm -rf %{buildroot}

%pre
if [ $1 = 1 ]; then
  %sysusers_create_compat %{SOURCE1}
fi

%files
%defattr(-,root,root,-)
%{_bindir}*
%{_mandir}/*
%{_datadir}/locale/*
%{_var}/*
%{_sysusersdir}/%{name}.sysusers

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 0.26-5
- Release bump for SRP compliance
* Sun Oct 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.26-4
- Create mlocate group
* Sat Jan 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 0.26-3
- Bump version as a part of gettext upgrade
* Thu Nov 15 2018 Sujay G <gsujay@vware.com> 0.26-2
- Added %check section
* Fri Jul 20 2018 Keerthana K <keerthanak@vmware.com> 0.26-1
- Initial mlocate package for Photon.
