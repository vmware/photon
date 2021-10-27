%global debug_package %{nil}

Summary:        Microsoft .NET Core Runtime
Name:           dotnet-runtime
Version:        5.0.11
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
# https://download.visualstudio.microsoft.com/download/pr/4652f15f-0061-4b13-aa61-0c1d23c3b290/af67e2036f0086a3794ba988233b41ae/dotnet-runtime-5.0.11-linux-x64.tar.gz
Source0:        %{name}-%{version}-linux-x64.tar.gz
%define sha1    %{name}=daea78f07caac8be6137bfdddca7057a9c9a6600

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
