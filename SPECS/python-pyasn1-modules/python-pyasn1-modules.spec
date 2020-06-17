%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A collection of ASN.1-based protocols modules.
Name:           python3-pyasn1-modules
Version:        0.2.2
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/pyasn1-modules
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        pyasn1-modules-%{version}.tar.gz
%define sha1    pyasn1-modules=a01ed1546373fd113c1ddf3ad686bbdf07251a00

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pyasn1
%endif
Requires:       python3-pyasn1
Requires:       python3
Requires:       python3-libs

%description
This is a small but growing collection of ASN.1 data structures expressed in Python terms using pyasn1 data model.

It’s thought to be useful to protocol developers and testers.

All modules are py2k/py3k-compliant.

If you happen to convert some ASN.1 module into pyasn1 that is not yet present in this collection and wish to contribute - please send it to me.

Written by Ilya Etingof <ilya@glas.net>.


%prep
%setup -q -n pyasn1-modules-%{version}
find . -iname "*.py" | xargs -I file sed -i '1s/python/python3/g' file

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
pushd ../tools
for file in ../test/*.sh; do
    [ -f "$file" ] && chmod +x "$file" && PYTHONPATH=%{buildroot}%{python3_sitelib} "$file"
done
popd

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 0.2.2-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.2.2-1
-   Update to version 0.2.2
*   Mon Aug 14 2017 Xiaolin Li <xiaolinl@vmware.com> 0.0.8-2
-   Fixed make check.
*   Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 0.0.8-1
-   Initial packaging for Photon
