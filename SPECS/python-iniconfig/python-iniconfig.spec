%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-iniconfig
Version:        1.0.1
Release:        1%{?dist}
Summary:        Brain-dead simple parsing of ini files
Group:          Development/Libraries
License:        MIT
URL:            http://github.com/RonnyPfannschmidt/iniconfig
Source0:        https://files.pythonhosted.org/packages/aa/6e/60dafce419de21f2f3f29319114808cac9f49b6c15117a419737a4ce3813/iniconfig-1.0.1.tar.gz
%define sha1 iniconfig=37bae0d794fb63afc8ed588d140d111224a75f54

Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools

Requires:       python3

Provides:       python3dist(iniconfig) = %{version}
Provides:       python3.8dist(iniconfig) = %{version}

%description
iniconfig: brain-dead simple parsing of ini files

%prep
%autosetup -n iniconfig-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sun Sep 20 2020 Susant Sahani <ssahani@vmware.com>  1.0.1-1
- Initial rpm release
