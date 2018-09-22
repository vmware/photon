%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-vcversioner
Version:        2.16.0.0
Release:        1%{?dist}
Summary:        Python version extractor
License:        ISC
Group:          Development/Languages/Python
Url:		https://github.com/habnabit/vcversioner
Source0:        vcversioner-%{version}.tar.gz
%define sha1    vcversioner=ce076b62e8f0772bf79f29762bfc3cf09f6781b5

BuildRequires: python2
#BuildRequires: python2-libs
BuildRequires: python-setuptools

BuildArch:      noarch

%description
Elevator pitch: you can write a setup.py with no version information specified, and vcversioner will find a recent, properly-formatted VCS tag and extract a version from it.

%package -n     python3-vcversioner
Summary:        python-vcversioner
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

%description -n python3-vcversioner
Python 3 version.

%prep
%setup -n vcversioner-%{version}
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
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
pushd ../p3dir
python3 setup test
popd

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-vcversioner
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Tue Oct 23 2018 Sujay G <gsujay@vmware.com> 2.16.0.0-1
-   Initial version
