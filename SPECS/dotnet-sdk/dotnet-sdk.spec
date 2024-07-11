%define debug_package %{nil}

Summary:        Microsoft .NET Core SDK
Name:           dotnet-sdk
Version:        8.0.206
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
# https://download.visualstudio.microsoft.com/download/pr/17b6759f-1af0-41bc-ab12-209ba0377779/e8d02195dbf1434b940e0f05ae086453/dotnet-sdk-6.0.100-linux-x64.tar.gz
Source0: %{name}-%{version}-linux-x64.tar.gz
%define sha512 %{name}=d03cbb5ea44a6f4957d7c1fa0f7c19e3df2efcbf569b071082e37ac86776af0729540c3bbddc44668ae2eedcfcb4b098883bb560d26418f1583a558d60c99ef5

BuildArch: x86_64

Requires: dotnet-runtime = 8.0.7
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
* Thu Jul 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 8.0.206-1
- Upgrade to v8.0.206
* Thu Jan 11 2024 Anmol Jain <anmolja@vmware.com> 8.0.101-2
- Bump version as a part to set env location
* Thu Jan 11 2024 Anmol Jain <anmolja@vmware.com> 8.0.101-1
- Version update
* Thu Dec 21 2023 Anmol Jain <anmolja@vmware.com> 7.0.404-1
- Upgrade version to 7.0.404
* Mon Jun 12 2023 Anmol Jain <anmolja@vmware.com> 7.0.203-1
- Upgrade version to 7.0.203
* Sun Feb 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.0.102-2
- Bump version as a part of icu upgrade
* Sat Feb 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.0.102-1
- Upgrade to v7.0.102
* Thu Oct 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.0.100-rc1.1
- Bump version as a part of icu upgrade
* Wed Oct 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.0.100-rc1
- Upgrade to v7.0.100-rc1
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
