%define debug_package %{nil}
Summary:        Altgraph helps in creating graph network for doing BFS and DFS traversals.
Name:           python3-altgraph
Version:        0.17.2
Release:        3%{?dist}
Url:            https://pypi.org/project/altgraph
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/22/5a/ac50b52581bbf0d8f6fd50ad77d20faac19a2263b43c60e7f3af8d1ec880/altgraph-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3

%description
altgraph is a fork of graphlib: a graph (network) package for constructing graphs, BFS and DFS traversals, topological sort, shortest paths, etc. with graphviz output.

%prep
%autosetup -p1 -n altgraph-%{version}

%build
%{py3_build}

%install
%{py3_install}

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.17.2-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.17.2-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.17.2-1
- Automatic Version Bump
* Wed Oct 14 2020 Piyush Gupta <gpiyush@vmware.com> 0.17-1
- Initial packaging
