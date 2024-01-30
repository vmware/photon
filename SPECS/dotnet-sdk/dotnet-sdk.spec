%define debug_package %{nil}

Summary:        Microsoft .NET Core SDK
Name:           dotnet-sdk
Version:        7.0.302
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
%define sha512 %{name}=9387bd804ed980ba1bc33093598ddbafa3a761e07d28916c94442cc329533d78a03bfc59d3066a1a861244302414e7e658b4e721b5bc825f623f8f908e748b7e

BuildArch: x86_64

BuildRequires: lttng-ust-devel >= 2.13.4-2

Requires: curl
Requires: libunwind
Requires: krb5
Requires: lttng-ust >= 2.13.4-2
Requires: icu >= 70.1
Requires: libstdc++

%description
.NET Core is a development platform that you can use to build command-line
applications, microservices and modern websites.

%prep
%autosetup -p1 -c %{name}-%{version} -p1

%build

%install
mkdir -p %{buildroot}%{_libdir}/dotnet/sdk

cp -pr sdk/%{version} %{buildroot}%{_libdir}/dotnet/sdk

%files
%defattr(-,root,root,0755)
%{_libdir}/*

%changelog
* Thu Jun 01 2023 Raymond Welch <rwelch@vmware.com> 7.0.302-1
- Upgrade to v7.0.302, removed the dotnet-runtime dependency, sdk installs the dotnet runtime.
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
