%define debug_package %{nil}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Altgraph helps in creating graph network for doing BFS and DFS traversals.
Name:           python3-altgraph
Version:        0.17
Release:        1%{?dist}
Url:            https://pypi.org/project/altgraph
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/22/5a/ac50b52581bbf0d8f6fd50ad77d20faac19a2263b43c60e7f3af8d1ec880/altgraph-%{version}.tar.gz
%define sha1    altgraph=8229b0fd463ff107e08e313d25a08c96b01fb635
BuildRequires:  python3
BuildRequires:  python3-setuptools
Requires:       python3

%description
altgraph is a fork of graphlib: a graph (network) package for constructing graphs, BFS and DFS traversals, topological sort, shortest paths, etc. with graphviz output.

%prep
%setup -q -n altgraph-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --root=%{buildroot}

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Wed Oct 14 2020 Piyush Gupta <gpiyush@vmware.com> 0.17-1
-   Initial packaging
