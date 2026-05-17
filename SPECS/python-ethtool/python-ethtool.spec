%global build_if %{photon_subrelease} >= 91

#
# spec file for package python3-ethtool
#

%global pypi_name ethtool
Name:           python3-ethtool
Version:        0.15
Release:        6%{?dist}
Summary:        Python module to interface with ethtool
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/ethtool/
Source0:        python-ethtool-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  libnl-devel
BuildRequires:  asciidoc3
BuildRequires:  libxslt
BuildRequires:  docbook-xsl
BuildRequires:  docbook-xml
BuildRequires: python3-defusedxml

%if 0%{?with_check}
BuildRequires: iproute2
BuildRequires: ethtool
%endif

Requires:      libnl
Requires:      python3

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
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.15-6
- Extended to build for subrelease 91 and above
* Fri Apr 17 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 0.15-5
- Remove deprecated net-tools from check BuildRequires
* Tue Mar 31 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 0.15-4
- Remove BuildRequires: xmlto; part of xmlto deprecation from >= 92
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.15-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.15-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.15-1
- Automatic Version Bump
* Sun Oct 11 2020 Prashant S Chauhan <psinghchauha@vmware.com> 0.14-3
- Build with updated ethtool release
* Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 0.14-2
- Use asciidoc3
* Thu Mar 19 2020 Shreyas B. <shreyasb@vmware.com> 0.14-1
- Initial version.
