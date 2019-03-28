%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           PyYAML
Version:        3.12
Release:        3%{?dist}
Summary:        YAML parser and emitter for Python
Group:          Development/Libraries
License:        MIT
URL:            http://pyyaml.org/
Source0:        http://pyyaml.org/download/pyyaml/%{name}-%{version}.tar.gz
%define sha1 PyYAML=cb7fd3e58c129494ee86e41baedfec69eb7dafbe
Patch0:         PyYAML-CVE-2017-18342.patch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  libyaml-devel

Requires:       python2
Requires:       python2-libs
Requires:       libyaml

%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that allow
to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistence.

%package -n     python3-PyYAML
Summary:        python3-PyYAML
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  libyaml-devel

Requires:       python3
Requires:       python3-libs
Requires:       libyaml

%description -n python3-PyYAML
Python 3 version.


%prep
%setup -q -n PyYAML-%{version}
%patch0 -p1
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
python2 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}
chmod a-x examples/yaml-highlight/yaml_hl.py
pushd ../p3dir
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}
chmod a-x examples/yaml-highlight/yaml_hl.py
popd

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc PKG-INFO README LICENSE examples
%{python2_sitelib}/*

%files -n python3-PyYAML
%defattr(-,root,root,-)
%doc PKG-INFO README LICENSE examples
%{python3_sitelib}/*


%changelog
*   Thu Mar 28 2019 Ankit Jain <ankitja@vmware.com> 3.12-3
-   Fix for CVE-2017-18342
*   Tue May 16 2017 Kumar Kaushik <kaushikk@vmware.com> 3.12-2
-   Adding python3 support.
*   Tue Apr 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.12-1
-   Updated version to 3.12
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.11-2
-   GA - Bump release of all rpms
*   Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
