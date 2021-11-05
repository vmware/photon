%define debug_package %{nil}

Summary:        Microsoft .NET Core SDK
Name:           dotnet-sdk
Version:        5.0.402
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
# https://github.com/dotnet/core/blob/main/release-notes/5.0/5.0.11/5.0.11.md
# https://download.visualstudio.microsoft.com/download/pr/6788a5a5-1879-4095-948d-72c7fbdf350f/c996151548ec9f24d553817db64c3577/dotnet-sdk-5.0.402-linux-x64.tar.gz
Source0:        %{name}-%{version}-linux-x64.tar.gz
%define sha1    %{name}=7d29824b0d6931724765b8dcf0c48b33582928ec

BuildArch:      x86_64

Requires:       dotnet-runtime
Requires:       icu

%description
.NET Core is a development platform that you can use to build command-line
applications, microservices and modern websites.

%prep
%autosetup -c dotnet-sdk-%{version} -p1

%build

%install
mkdir -p %{buildroot}%{_libdir}/dotnet/sdk %{buildroot}%{_docdir}/%{name}-%{version}
cp -r sdk/%{version} %{buildroot}%{_libdir}/dotnet/sdk
cp LICENSE.txt ThirdPartyNotices.txt %{buildroot}%{_docdir}/dotnet-sdk-%{version}

%files
%defattr(-,root,root,0755)
%{_libdir}/*
%{_docdir}/*

%changelog
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
