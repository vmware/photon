%global debug_package %{nil}

Name:           tinydir
Version:        1.2.5
Release:        1%{?dist}
Summary:        Portable and easy to integrate C directory and file reader
License:        BSD
URL:            https://github.com/cxong/%{name}
Vendor:         VMware, Inc.
Group:          Development/Tools
Distribution:   Photon

Source0: %{url}/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=d86a8709b92c9b6847bd85b4b307a411edf30156a06557641a051f74a7c19898451616772ee53ad2d8fc6c2ea2285c4c4edf2197f36cf48ede6d539d24ebb2cf

BuildRequires: cmake

%description
Lightweight, portable and easy to integrate C directory and file reader.
TinyDir wraps dirent for POSIX and FindFirstFile for Windows.

%package devel
Summary:        Header & devel files of %{name}
Provides:       %{name} = %{version}-%{release}

BuildArch:      noarch

%description devel
%{summary}

%prep
%autosetup -p1

%build

%install
mkdir -p %{buildroot}%{_includedir}
cp %{name}.h %{buildroot}%{_includedir}

mkdir -p %{buildroot}%{_datadir}/pkgconfig/

# Install pkg-config file.
cat << EOF > %{buildroot}%{_datadir}/pkgconfig/%{name}.pc
prefix=%{_prefix}
exec_prefix=\${prefix}

includedir=%{_includedir}

Name: %{name}
Version: %{version}
Description: Portable and easy to integrate C directory and file reader
EOF

# Clean-up for including samples in %%doc.
rm -f samples/{.gitignore,CMakeLists.txt}

%check
export CTEST_OUTPUT_ON_FAILURE=1
pushd tests
cmake -DCMAKE_VERBOSE_MAKEFILE=ON .
%make_build
ctest
popd

%files devel
%defattr(-,root,root)
%license COPYING
%doc samples/ package.json README.md
%{_includedir}/%{name}.h
%{_datadir}/pkgconfig/%{name}.pc

%changelog
* Wed Nov 29 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.2.5-1
- Initial version. Needed by sysdig.
