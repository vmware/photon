Summary:	A C++ JSON Parser/Generator
Name:		json_spirit
Version:	4.08
Release:	3%{?dist}
License:	MIT
URL:		https://www.codeproject.com/Articles/20027/JSON-Spirit-A-C-JSON-Parser-Generator-Implemented
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon

Source0:	https://www.codeproject.com/KB/recipes/JSON_Spirit/json_spirit_v4.08.zip
%define sha1 %{name}=d46a896991b7eb736bff2628909645d3bbaaf5cf

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  boost
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  unzip

Requires:       boost

%description
JSON Spirit is a C++ library that reads and writes JSON files or streams. It
is written using the Boost Spirit parser generator.

%package devel
Summary:        json_spirit devel
Group:          Development/Tools
%description devel
This contains development tools and libraries for json_spirit.

%prep
%autosetup -n json_spirit_v%{version} -p1

%build
mkdir -p build
cd build
# Build static lib
cmake -DCMAKE_INSTALL_PREFIX=/usr ..
make CXX_FLAGS='-std=c++98'
# Build shared lib
pushd ../json_spirit
sed -i s/"json_spirit STATIC"/"json_spirit SHARED"/g CMakeLists.txt
popd
cmake ..
make CXX_FLAGS='-std=c++98 -fPIC' %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} install
install -v -D json_spirit/libjson_spirit.so -t %{buildroot}%{_libdir}

%files
%defattr(-,root,root)
%{_libdir}/libjson_spirit.so*

%files devel
%defattr(-,root,root)
%{_includedir}/json_spirit*
%{_libdir}/libjson_spirit.a

%changelog
* Fri Oct 29 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.08-3
- Bump version as a part of boost upgrade
* Thu Jun 1  2017 Bo Gan <ganb@vmware.com> 4.08-2
- Fix file paths
* Sat Mar 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.08-1
- Initial version of json_spirit for Photon.
