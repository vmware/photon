%global debug_package %{nil}

Summary:        Microsoft .NET Core Runtime
Name:           dotnet-runtime
Version:        6.0.26
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
Url:            https://github.com/dotnet/core
Group:          Development/Tools

# Download source tarball from the links provided in:
# https://github.com/dotnet/core/tree/main/release-notes
#
# For example:
# https://github.com/dotnet/core/blob/main/release-notes/6.0/6.0.0/6.0.0.md
# https://download.visualstudio.microsoft.com/download/pr/0ce1c34f-0d9e-4d9b-964e-da676c8e605a/7a6c353b36477fa84f85b2821f2350c2/dotnet-runtime-6.0.0-linux-x64.tar.gz
Source0:        %{name}-%{version}-linux-x64.tar.gz
%define sha512    %{name}=7336f71f7f99ffc3a44c7d730c6a1e08c5c0b6e05d2076a1963776f174f8588d31c9b783d1c4f645f7e7cc6a54077b798c6bde35ed4a812ffd9b2427d29b0b34
BuildArch:      x86_64

Requires:       curl
Requires:       libunwind
Requires:       krb5
Requires:       lttng-ust

%description
.NET Core is a development platform that you can use to build command-line
applications, microservices and modern websites.

%prep
%autosetup -c dotnet-runtime-%{version} -p1

%build

%install
mkdir -p %{buildroot}%{_libdir}/dotnet %{buildroot}%{_docdir}/dotnet-runtime-%{version}
cp -r * %{buildroot}%{_libdir}/dotnet
mkdir -p %{buildroot}%{_bindir}
cp LICENSE.txt ThirdPartyNotices.txt %{buildroot}%{_docdir}/dotnet-runtime-%{version}
rm LICENSE.txt ThirdPartyNotices.txt
ln -sf %{_libdir}/dotnet/dotnet %{buildroot}%{_bindir}/dotnet

%pre

%post
/sbin/ldconfig

%preun

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,0755)
%exclude %{_libdir}/debug
%{_docdir}/*
%{_bindir}/dotnet
%{_libdir}/*

%changelog
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
