%define debug_package %{nil}
%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Altgraph helps in creating graph network for doing BFS and DFS traversals.
Name:           python-altgraph
Version:        0.17
Release:        1%{?dist}
Url:            https://pypi.org/project/altgraph
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/22/5a/ac50b52581bbf0d8f6fd50ad77d20faac19a2263b43c60e7f3af8d1ec880/altgraph-%{version}.tar.gz
%define sha1    altgraph=8229b0fd463ff107e08e313d25a08c96b01fb635
BuildRequires:  python2
BuildRequires:  python-xml
BuildRequires:  python-setuptools

BuildRequires:  python3
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools

Requires:       python2

%description
altgraph is a fork of graphlib: a graph (network) package for constructing graphs, BFS and DFS traversals, topological sort, shortest paths, etc. with graphviz output.

%package -n     python3-altgraph
Summary:        python3-altgraph
Requires:       python3

%description -n python3-altgraph
Python 3 version.

%prep
%setup -q -n altgraph-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --skip-build --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-altgraph
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Thu Feb 11 2021 Ankit Jain <ankitja@vmware.com> 0.17-1
-   Initial packaging
