%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-chardet
Version:        3.0.4
Release:        1%{?dist}
Summary:        Character encoding auto-detection in Python
License:        LGPLv2
URL:            https://github.com/chardet
Source0:        https://pypi.org/project/chardet/chardet-%{version}.tar.gz
%define sha1    chardet=4766fb07e700945a7085d073257f1f320d037ce8
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pytest
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-xml

%description
Character encoding auto-detection in Python. As\
smart as your browser. Open source.

%package -n python2-chardet
Summary: Character encoding auto-detection in Python
%description -n python2-chardet
Character encoding auto-detection in Python. As\
smart as your browser. Open source.

%package -n python3-chardet
Summary:        Character encoding auto-detection in Python 3
%description -n python3-chardet
Character encoding auto-detection in Python. As 
smart as your browser. Open source.
Python 3 version.

%prep
%setup -n chardet-%{version}
sed -ie '1d' chardet/cli/chardetect.py

%build
python2 setup.py build
python3 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
rm %{buildroot}%{_bindir}/*
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
python3 setup.py test

%files -n python2-chardet
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-chardet
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/chardetect

%changelog
*   Wed Sep 19 2018 Ajay Kaher <akaher@vmware.com> 18.3-1
-   Upgraded version to 18.3


