%define debug_package %{nil}

Summary:        Microsoft .NET Core SDK
Name:           dotnet-sdk
Version:        8.0.420
Release:        2%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
Url:            https://github.com/dotnet/core
Group:          Development/Tools

BuildArch: x86_64

# Download source tarball from the links provided in:
# https://github.com/dotnet/core/tree/main/release-notes
#
# For example:
# https://github.com/dotnet/core/blob/main/release-notes/6.0/6.0.0/6.0.0.md
# https://download.visualstudio.microsoft.com/download/pr/17b6759f-1af0-41bc-ab12-209ba0377779/e8d02195dbf1434b940e0f05ae086453/dotnet-sdk-6.0.100-linux-x64.tar.gz
Source0: %{name}-%{version}-linux-x64.tar.gz
%define sha512 %{name}=36c68c1be9d5c6f24cd8e6bd4b6d36bfd7ab724ac7e3499fb13e42e70a9003310e5ee5759ed19ced1f0ecd3d26a55f135c7e72d6f788e7d44f5f0eaa72ad9a07

Requires: dotnet-runtime = 8.0.28
Requires: icu >= 70.1

%description
.NET Core is a development platform that you can use to build command-line
applications, microservices and modern websites.

%prep
%autosetup -p1 -c %{name}-%{version} -p1

%build

%install
mkdir -p %{buildroot}%{_libdir}/dotnet/sdk \
         %{buildroot}%{_sysconfdir}/dotnet

cp -a sdk/%{version} %{buildroot}%{_libdir}/dotnet/sdk
echo "%{_libdir}/dotnet" > %{buildroot}%{_sysconfdir}/dotnet/install_location

%files
%defattr(-,root,root,0755)
%{_libdir}/*
%{_sysconfdir}/dotnet/install_location

%changelog
* Mon Jun 15 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 8.0.420-2
- Bump version as a part of dotnet-runtime upgrade
* Thu Apr 23 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 8.0.420-1
- Upgrade to v8.0.420
* Fri May 16 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.0.428-1
- Upgrade to v6.0.428
* Mon Jan 22 2024 Anmol Jain <anmolja@vmware.com> 6.0.418-1
- Upgarde to version 6.0.418
* Wed Dec 20 2023 Anmol Jain <anmolja@vmware.com> 6.0.417-1
- Upgarde to version 6.0.417
* Mon Oct 31 2022 Anmol Jain <anmolja@vmware.com> 6.0.402-1
- Upgarde to version 6.0.402
* Mon Oct 31 2022 Anmol Jain <anmolja@vmware.com> 6.0.105-1
- Upgrade to version 6.0.105
* Tue Dec 07 2021 Alexey Makhalov <amakhalov@vmware.com> 6.0.100-2
- Release bump to build with icu-70.1
* Mon Nov 15 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 6.0.100-1
- Upgrade to version 6.0.100
* Tue Oct 26 2021 Shreenidhi Shedi <sshedi@vmware.com> 5.0.402-1
- Upgrade to version 5.0.402
* Tue Mar 9 2021 Shreyas B. <shreyasb@vmware.com> 5.0.103-1
- upgrade to version 5.0.103
* Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1.201-1
- Automatic Version Bump
* Thu Nov 07 2019 Shreyas B. <shreyasb@vmware.com> 2.1.509-1
- upgraded to version 2.1.509
* Wed Dec 05 2018 Ajay Kaher <akaher@vmware.com> 2.1.403-1
- upgraded to version 2.1.403
* Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.4-1
- Initial build for photon
