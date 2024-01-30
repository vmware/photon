%global debug_package %{nil}

Summary:        Microsoft ASP.NET Core Runtime
Name:           aspnetcore-runtime
Version:        7.0.5
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
Url:            https://github.com/dotnet/aspnetcore
Group:          Development/Tools

# Download source tarball from the links provided in:
# https://github.com/dotnet/core/tree/main/release-notes
#
# For example:
# https://github.com/dotnet/core/blob/main/release-notes/6.0/6.0.0/6.0.0.md
# https://download.visualstudio.microsoft.com/download/pr/0ce1c34f-0d9e-4d9b-964e-da676c8e605a/7a6c353b36477fa84f85b2821f2350c2/dotnet-runtime-6.0.0-linux-x64.tar.gz
Source0: %{name}-%{version}-linux-x64.tar.gz
%define sha512 %{name}=859d48d0f29e014d56e89161d8001f75b3b0b03ee04f86641066570cfbe267b06798232500a86fd7bc31edf022097278dfeb496874778fead4476863aa994928

BuildArch: x86_64

BuildRequires: lttng-ust-devel >= 2.13.4-2

Requires: curl
Requires: libunwind
Requires: krb5
Requires: lttng-ust >= 2.13.4-2
Requires: libstdc++

%description
ASP.NET Core is an open-source and cross-platform framework for building modern
cloud-based internet-connected applications, such as web apps, IoT apps, and mobile backends.

%prep
%autosetup -p1 -c %{name}-%{version} -p1

%build

%install
mkdir -p %{buildroot}%{_libdir}/dotnet \
         %{buildroot}%{_docdir}/%{name}-%{version} \
         %{buildroot}%{_bindir}

cp -pr * %{buildroot}%{_libdir}/dotnet
ln -sfrv %{buildroot}%{_libdir}/dotnet/dotnet %{buildroot}%{_bindir}/dotnet

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,0755)
%exclude %dir %{_libdir}/debug
%{_docdir}/*
%{_bindir}/dotnet
%{_libdir}/*

%changelog
* Thu Jun 01 2023 Raymond Welch <rwelch@vmware.com> 7.0.5-1
- Initial build for photon
