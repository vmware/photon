Summary:        Text editor
Name:           nano
Version:        6.2
Release:        1%{?dist}
License:        GPLv3+
URL:            http://www.nano-editor.org/
Group:          Applications/Editors
Source0:        http://www.nano-editor.org/dist/v3/%{name}-%{version}.tar.xz
%define sha512  nano=cee43c7e72fa9dbfc79fd5c602eb37cba55c8cde849a3bfd283c0dc3d35162f46551a0401b9f865c6f7d5c6dce6e7a894d97e22a4e6729cd20b9929221b46583
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  ncurses-devel
Requires:       ncurses

%description
The Nano package contains a small, simple text editor

%package        lang
Summary:        Lang for nano
Requires:       %{name} = %{version}

%description    lang
Lang for nano

%prep
%autosetup

%build
%configure \
            --enable-utf8     \
            --docdir=%{_docdir}/%{name}-%{version}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install
install -v -m644 %{_builddir}/%{name}-%{version}/doc/sample.nanorc %{_sysconfdir}
install -v -m644 %{_builddir}/%{name}-%{version}/doc/nano.html %{_docdir}/%{name}-%{version}.html
%find_lang %{name}

%check
make %{?_smp_mflags} check

%files lang -f %{name}.lang
%defattr(-,root,root)

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man*/*
%{_infodir}/*
%{_datadir}/nano/*
%{_datadir}/doc/%{name}-%{version}/*
# conflict with parted-3.2-8.ph3
%exclude %{_infodir}/dir

%changelog
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 6.2-1
-   Automatic Version Bump
*   Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 5.7-1
-   Automatic Version Bump
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 5.6.1-1
-   Automatic Version Bump
*   Wed Aug 26 2020 Gerrit Photon <photon-checkins@vmware.com> 5.2-2
-   Fix spec configures
*   Wed Aug 26 2020 Gerrit Photon <photon-checkins@vmware.com> 5.2-1
-   Automatic Version Bump
*   Wed Aug 12 2020 Gerrit Photon <photon-checkins@vmware.com> 5.1-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 5.0-1
-   Automatic Version Bump
*   Wed Sep 12 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 3.0-1
-   Update package version
*   Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 2.8.0-1
-   Update package version
*   Mon Oct 03 2016 ChangLee <changlee@vmware.com> 2.5.2-3
-   Modified check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5.2-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 2.5.2-1
-   Updating to new version.
*   Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 2.2.6.2
-   Handled locale files with macro find_lang
*   Tue Dec 30 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.2.6-1
-   Initial build. First version.
