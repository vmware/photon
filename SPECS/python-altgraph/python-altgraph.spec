%global build_if %{photon_subrelease} >= 92

%define debug_package %{nil}
Summary:        Altgraph helps in creating graph network for doing BFS and DFS traversals.
Name:           python3-altgraph
Version:        0.17.5
Release:        1%{?dist}
Url:            https://pypi.org/project/altgraph
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0: https://github.com/ronaldoussoren/altgraph/archive/refs/tags/v%{version}.tar.gz#/altgraph-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-packaging
Requires:       python3

%description
altgraph is a fork of graphlib: a graph (network) package for constructing graphs, BFS and DFS traversals, topological sort, shortest paths, etc. with graphviz output.

%prep
%autosetup -p1 -n altgraph-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%files -f %{py_ghost_filelist}
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Thu Oct 29 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.17.5-1
- Upgrade to 0.17.5
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.17.2-5
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.17.2-4
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.17.2-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.17.2-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.17.2-1
- Automatic Version Bump
* Wed Oct 14 2020 Piyush Gupta <gpiyush@vmware.com> 0.17-1
- Initial packaging
