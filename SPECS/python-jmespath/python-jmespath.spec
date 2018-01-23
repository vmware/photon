%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Summary:        Query Language for JSON
Name:           python-jmespath
Version:        0.9.3
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/jmespath
Source0:        https://pypi.python.org/packages/e5/21/795b7549397735e911b032f255cff5fb0de58f96da794274660bca4f58ef/jmespath-%{version}.tar.gz
%define         sha1 jmespath=eca7ba2e8d4fc50239973b59e07f9f527e0c0839
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-xml
Requires:       python2
Requires:       python2-libs
BuildArch:      noarch

%description
JMESPath (pronounced “james path”) allows you to declaratively specify how to extract elements from a JSON document.

%package -n     python3-jmespath
Summary:        python-jmespath
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-jmespath
Python 3 version.

%prep
%setup -q -n jmespath-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}
for item in %{buildroot}/%{_bindir}/*
    do mv ${item} "${item}-%{python3_version}" ;
done
popd
python2 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*
%{_bindir}/jp.py

%files -n  python3-jmespath
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/jp.py-%{python3_version}

%changelog
*   Sun Jan 07 2018 Kumar Kaushik <kaushikk@vmware.com> 0.9.3-1
-   Initial packaging for photon.
