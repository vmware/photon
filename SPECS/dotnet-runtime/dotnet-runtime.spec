%global debug_package %{nil}

Summary:        Microsoft .NET Core Runtime
Name:           dotnet-runtime
Version:        6.0.36
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
Url:            https://github.com/dotnet/core
Group:          Development/Tools

BuildArch:      x86_64

# Download source tarball from the links provided in:
# https://github.com/dotnet/core/tree/main/release-notes
#
# For example:
# https://github.com/dotnet/core/blob/main/release-notes/6.0/6.0.0/6.0.0.md
# https://download.visualstudio.microsoft.com/download/pr/0ce1c34f-0d9e-4d9b-964e-da676c8e605a/7a6c353b36477fa84f85b2821f2350c2/dotnet-runtime-6.0.0-linux-x64.tar.gz
Source0: %{name}-%{version}-linux-x64.tar.gz
%define sha512 %{name}=afb6018fcabec468ccd7ae2f1131d8c9de7f4de7645b8f0c223efbbdbfdc515fb0642a399ebfe372c02044416c4cae463c9c802cd156b9da4181efff0e33ee94

Requires:       curl
Requires:       libunwind
Requires:       krb5
Requires:       lttng-ust

%description
.NET Core is a development platform that you can use to build command-line
applications, microservices and modern websites.

%prep
%autosetup -c %{name}-%{version} -p1

%build

%install
mkdir -p %{buildroot}%{_libdir}/dotnet \
         %{buildroot}%{_docdir}/%{name}-%{version} \
         %{buildroot}%{_bindir}

cp -a * %{buildroot}%{_libdir}/dotnet
cp LICENSE.txt ThirdPartyNotices.txt %{buildroot}%{_docdir}/%{name}-%{version}
ln -sfrv %{_libdir}/dotnet/dotnet %{buildroot}%{_bindir}/dotnet

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,0755)
%exclude %{_libdir}/debug
%{_docdir}/*
%{_bindir}/dotnet
%{_libdir}/*

%changelog
* Fri May 16 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.0.36-1
- Upgrade to v6.0.36
* Mon Jan 22 2024 Anmol Jain <anmolja@vmware.com> 6.0.26-1
- Upgarde to version 6.0.26
* Wed Dec 20 2023 Anmol Jain <anmolja@vmware.com> 6.0.25-1
- Upgarde to version 6.0.25
* Thu Nov 03 2022 Anmol Jain <anmolja@vmware.com> 6.0.10-1
- Upgrade to version 6.0.10
* Mon Oct 31 2022 Anmol Jain <anmolja@vmware.com> 6.0.5-1
- Upgrade to version 6.0.5
* Mon Nov 15 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 6.0.0-1
- Upgrade to version 6.0.0
* Tue Oct 26 2021 Shreenidhi Shedi <sshedi@vmware.com> 5.0.11-1
- Upgrade to version 5.0.11
* Tue Mar 9 2021 Shreyas B. <shreyasb@vmware.com> 5.0.3-1
- Upgrade to v5.0.3
* Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1.5-1
- Automatic Version Bump
* Mon Nov 11 2019 Shreyas B. <shreyasb@vmware.com> 2.2.3-1
- Upgraded to v2.2.3
* Wed Dec 05 2018 Ajay Kaher <akaher@vmware.com> 2.2.0-1
- upgraded to version 2.2.0
* Thu Sep 27 2018 Ajay Kaher <akaher@vmware.com> 2.1.4-1
- upgraded to version 2.1.4
- add aarch64 support
* Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.5-1
- Initial build for photon
