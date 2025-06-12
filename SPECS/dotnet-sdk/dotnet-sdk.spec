%define debug_package %{nil}

Summary:        Microsoft .NET Core SDK
Name:           dotnet-sdk
Version:        6.0.428
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
# https://github.com/dotnet/core/blob/main/release-notes/5.0/5.0.11/5.0.11.md
# https://download.visualstudio.microsoft.com/download/pr/6788a5a5-1879-4095-948d-72c7fbdf350f/c996151548ec9f24d553817db64c3577/dotnet-sdk-5.0.402-linux-x64.tar.gz
Source0: %{name}-%{version}-linux-x64.tar.gz
%define sha512 %{name}=04395f991ab50e4755ce1ae53e23592a7420b71b82160883bae3194dd1dfd5dcaed78743e4e0b4dd51ea43c49ec84b5643630707b3854f1471265dc98490d2f9

Requires: dotnet-runtime = 6.0.36
Requires: icu

%description
.NET Core is a development platform that you can use to build command-line
applications, microservices and modern websites.

%prep
%autosetup -c %{name}-%{version} -p1

%build

%install
mkdir -p %{buildroot}%{_libdir}/dotnet/sdk \
         %{buildroot}%{_docdir}/%{name}-%{version}

cp -a sdk/%{version} %{buildroot}%{_libdir}/dotnet/sdk
cp LICENSE.txt ThirdPartyNotices.txt %{buildroot}%{_docdir}/%{name}-%{version}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,0755)
%{_libdir}/*
%{_docdir}/*

%changelog
* Thu Jun 12 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.0.428-1
- Upgrade to v6.0.428
* Mon Jan 22 2024 Anmol Jain <anmolja@vmware.com> 6.0.418-1
- Upgarde to version 6.0.418
* Tue Jan 09 2024 Anmol Jain <anmolja@vmware.com> 6.0.417-1
- Upgarde to version 6.0.417
* Tue Nov 15 2022 Anmol Jain <anmolja@vmware.com> 5.0.407-1
- Upgrade to version 5.0.407
* Tue Oct 26 2021 Shreenidhi Shedi <sshedi@vmware.com> 5.0.402-1
- Upgrade to version 5.0.402
* Tue Sep 21 2021 Shreyas B. <shreyasb@vmware.com> 5.0.400-1
- upgrade to v5.0.400
* Mon Jan 18 2021 Shreyas B. <shreyasb@vmware.com> 5.0.103-1
- upgrade to version 5.0.103
* Fri Oct 16 2020 Ashwin H <ashwinh@vmware.com> 3.1.201-2
- Bump up to use new icu lib.
* Sat Apr 11 2020 Shreyas B. <shreyasb@vmware.com> 3.1.201-1
- upgrade to version 3.1.201
* Thu Nov 07 2019 Shreyas B. <shreyasb@vmware.com> 2.1.509-1
- upgraded to version 2.1.509
* Wed Dec 05 2018 Ajay Kaher <akaher@vmware.com> 2.1.403-1
- upgraded to version 2.1.403
* Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.4-1
- Initial build for photon
