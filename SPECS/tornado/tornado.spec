%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           tornado
Version:        4.5.2
Release:        3%{?dist}
Summary:        Tornado is a Python web framework and asynchronous networking library
License:        PSFL
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/tornado
Source0:        https://github.com/tornadoweb/tornado/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  tornado=d98ba7a9bb59c05a8ecdc02620c5c8ddfbeeec967edaecbe300ffd3118a1e3973c4eaf962abfc0aa080969228c22e643021818312ccd9a8cb4115cd56795d252

Patch0:         CVE-2023-28370.patch

Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python2
Requires:       python2-libs

%description

%package -n     python3-tornado
Summary:        python3 version
Requires:       python3
Requires:       python3-libs

%description -n python3-tornado
Python 3 version.

%prep
%autosetup -p1 -n tornado-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-tornado
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Wed Sep 13 2023 Kuntal Nayak <nkuntal@vmware.com> 4.5.2-3
-   Patch fixed CVE-2023-28370
*   Tue Dec 17 2019 Padmini Thirumalachar <pthirumalachar@vmware.com> 4.5.2-2
-   To build python2 and python3 tornado packages
-   To remove buildArch
*   Mon Dec 11 2017 Padmini Thirumalachar <pthirumalachar@vmware.com> 4.5.2-1
-   Initial version of python tornado for PhotonOS.
