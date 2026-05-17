%global build_if %{photon_subrelease} >= 91
Summary:        Header files from the SPIR-V registry
Name:           spirv-headers
Version:        1.4.341.0
Release:        2%{?dist}
URL:            https://github.com/KhronosGroup/SPIRV-Headers/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/KhronosGroup/SPIRV-Headers/archive/refs/tags/SPIRV-Headers-vulkan-sdk-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
%autosetup -p1 -n SPIRV-Headers-vulkan-sdk-%{version}

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
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.4.341.0-2
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 1.4.341.0-1
- Update to 1.4.341.0
* Thu Jun 26 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.313.0-1
- Upgrade to be compatible with spirv-llvm-translator
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 1.3.231.1-2
- Release bump for SRP compliance
* Tue Nov 15 2022 Shivani Agarwal <shivania2@vmware.com> 1.3.231.1-1
- initial version
