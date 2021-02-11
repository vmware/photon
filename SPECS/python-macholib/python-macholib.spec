%define debug_package %{nil}
%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        macholib can be used to analyze and edit Mach-O headers
Name:           python-macholib
Version:        1.14
Release:        1%{?dist}
Url:            https://pypi.org/project/macholib
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/0d/fe/61e8f6b569c8273a8f2dd73921738239e03a2acbfc55be09f8793261f269/macholib-%{version}.tar.gz
%define sha1    macholib=cc7c2936570780208d1521d49a8e90634ba69ee0
BuildRequires:  python2
BuildRequires:  python-xml
BuildRequires:  python-setuptools

BuildRequires:  python3
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools

Requires:       python2

%description
macholib can be used to analyze and edit Mach-O headers, the executable format used by Mac OS X

%package -n     python3-macholib
Summary:        python3-macholib
Requires:       python3

%description -n python3-macholib
Python 3 version.

%prep
%setup -q -n macholib-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/macho_dump %{buildroot}/%{_bindir}/macho_dump3
mv %{buildroot}/%{_bindir}/macho_find %{buildroot}/%{_bindir}/macho_find3
mv %{buildroot}/%{_bindir}/macho_standalone %{buildroot}/%{_bindir}/macho_standalone3
popd
python2 setup.py install --skip-build --root=%{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/macho_dump
%{_bindir}/macho_find
%{_bindir}/macho_standalone
%{python2_sitelib}/*

%files -n python3-macholib
%defattr(-,root,root,-)
%{_bindir}/macho_dump3
%{_bindir}/macho_find3
%{_bindir}/macho_standalone3
%{python3_sitelib}/*

%changelog
*   Thu Feb 11 2021 Ankit Jain <ankitja@vmware.com> 1.14-1
-   Initial packaging
