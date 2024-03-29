#
# spec file for package python3-ethtool
#

%global pypi_name ethtool
Name:           python3-ethtool
Version:        0.15
Release:        1%{?dist}
Summary:        Python module to interface with ethtool
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
License:        GPLv2
URL:            https://pypi.org/project/ethtool/
Source0:        python-ethtool-%{version}.tar.gz
%define sha512  python-ethtool=82a9c08d1794f8f44e2a797d4631bacef3d492c8274d161f74d789e299f3de4830e03e863e428a14dea9713c43f10a1c743a30a504bb4c8eac03bded5c708670

BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  libnl-devel
BuildRequires:  asciidoc3
# For 'xml'
BuildRequires: docbook-xml
BuildRequires: xmlto
BuildRequires: python3-defusedxml
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
%autosetup -n python-%{pypi_name}-%{version}

%build
%py3_build
a2x3 -d manpage -f manpage man/pethtool.8.asciidoc
a2x3 -d manpage -f manpage man/pifconfig.8.asciidoc

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
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.15-1
- Automatic Version Bump
* Sun Oct 11 2020 Prashant S Chauhan <psinghchauha@vmware.com> 0.14-3
- Build with updated ethtool release
* Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 0.14-2
- Use asciidoc3
* Thu Mar 19 2020 Shreyas B. <shreyasb@vmware.com> 0.14-1
- Initial version.
