Summary:        A collection of ASN.1-based protocols modules.
Name:           python3-pyasn1-modules
Version:        0.2.8
Release:        3%{?dist}
Url:            https://pypi.python.org/pypi/pyasn1-modules
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        pyasn1-modules-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_check}
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
%autosetup -n pyasn1-modules-%{version}
find . -iname "*.py" | xargs -I file sed -i '1s/python/python3/g' file

%build
%py3_build

%install
%py3_install

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.2.8-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.2.8-2
- Update release to compile with python 3.11
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.2.8-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 0.2.2-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.2.2-1
- Update to version 0.2.2
* Mon Aug 14 2017 Xiaolin Li <xiaolinl@vmware.com> 0.0.8-2
- Fixed make check.
* Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 0.0.8-1
- Initial packaging for Photon
