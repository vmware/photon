#
# spec file for package python3-ethtool
#

%{!?python3_sitearch: %define python3_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%global pypi_name ethtool
Name:           python3-ethtool
Version:        0.14
Release:        1%{?dist}
Summary:        Python module to interface with ethtool
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
License:        GPLv2
URL:            https://github.com/fedora-python/python-ethtool
Source0:        python-ethtool-%{version}.tar.gz
%define sha1 python-ethtool=6e811ede779f2eac9d30950b6dc7abba61372262

BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  libnl-devel
BuildRequires:  asciidoc
# For 'xml'
BuildRequires: docbook-xml
BuildRequires: xmlto
BuildRequires: python3-defusedxml
BuildRequires: python-defusedxml
Requires:      libnl

%if %{with_check}
BuildRequires: net-tools
BuildRequires: ethtool
%endif

%description
Python 3 bindings for the ethtool kernel interface, that allows querying and
changing of Ethernet card settings, such as speed, port, auto-negotiation, and
PCI locations.

%prep
%autosetup -n %{pypi_name}-%{version}

%build
python3 setup.py build
a2x -d manpage -f manpage man/pethtool.8.asciidoc
a2x -d manpage -f manpage man/pifconfig.8.asciidoc

%install
python3 setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}{%{_bindir},%{_sbindir}}/pifconfig
mv %{buildroot}{%{_bindir},%{_sbindir}}/pethtool

mkdir -p %{buildroot}%{_mandir}/man8/
cp -p man/*.8 %{buildroot}%{_mandir}/man8/

%check
export PYTHONPATH=%{buildroot}%{python3_sitearch}
LANG=en_US.UTF-8 python3 tests/parse_ifconfig.py -v
LANG=en_US.UTF-8 python3 -m unittest discover -v

%files
%defattr(0755,root,root,0755)
%doc README.rst CHANGES.rst
%license COPYING
%{_sbindir}/pifconfig
%{_sbindir}/pethtool
%doc %{_mandir}/man8/*
%{python3_sitearch}/%{pypi_name}.cpython-*.so
%{python3_sitearch}/%{pypi_name}-%{version}-py*.egg-info

%changelog
*   Thu Mar 19 2020 Shreyas B. <shreyasb@vmware.com> 0.14-1
-   Initial version.
