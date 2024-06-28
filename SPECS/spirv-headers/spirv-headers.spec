Summary:        Header files from the SPIR-V registry
Name:           spirv-headers
Version:        1.3.231.1
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/KhronosGroup/SPIRV-Headers/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/KhronosGroup/SPIRV-Headers/archive/refs/tags/SPIRV-Headers-%{version}.tar.gz
%define sha512  SPIRV-Headers-%{version}.tar.gz=d2c47127fd81430383e8656917f76933b713ca6cb93b2a9c16c9e0b125e2f62f8c497cab3a4fcc2a711decd911ec5d15f1eb0270add05442aff6672e08c890d7

BuildArch:      noarch

%description
Header files from the SPIR-V registry

This includes:

* Header files for various languages.
* JSON files describing the grammar for the SPIR-V core instruction
  set, and for the GLSL.std.450 extended instruction set.
* The XML registry file

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}

%description    devel
This includes:

* Header files for various languages.
* JSON files describing the grammar for the SPIR-V core instruction
  set, and for the GLSL.std.450 extended instruction set.
* The XML registry file

%prep
%autosetup -p1 -n SPIRV-Headers-sdk-%{version}

chmod a-x include/spirv/1.2/spirv.py

%build

%install
mkdir -p %buildroot%{_includedir}/
mv include/* %buildroot%{_includedir}/

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)

%files devel
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_includedir}/spirv/

%changelog
*   Tue Nov 15 2022 Shivani Agarwal <shivania2@vmware.com> 1.3.231.1-1
-   initial version
