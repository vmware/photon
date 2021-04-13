%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%define debug_package %{nil}

Name:           python3-PyYAML
Version:        5.3.1
Release:        1%{?dist}
Summary:        YAML parser and emitter for Python
Group:          Development/Libraries
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://pyyaml.org/
Source0:        http://pyyaml.org/download/pyyaml/PyYAML-%{version}.tar.gz
%define sha1 PyYAML=3b20272e119990b2bbeb03815a1dd3f3e48af07e
BuildRequires:  libyaml-devel
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
Requires:       python3-setuptools
Requires:       python3
Requires:       python3-libs
Requires:       libyaml

Provides:       python3.9dist(pyyaml)

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

%prep
%setup -q -n PyYAML-%{version}


%build
python3 setup.py build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}
chmod a-x examples/yaml-highlight/yaml_hl.py

%check
python3 setup.py test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc PKG-INFO README LICENSE examples
%{python3_sitelib}/*


%changelog
*   Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 5.3.1-1
-   Automatic Version Bump
*   Wed Jan 27 2021 Tapas Kundu <tkundu@vmware.com> 5.4.1-1
-   Update to 5.4.1
*   Wed Dec 16 2020 Shreenidhi Shedi <sshedi@vmware.com> 5.3.1-2
-   Fix build with new rpm
*   Wed Jul 29 2020 Gerrit Photon <photon-checkins@vmware.com> 5.3.1-1
-   Automatic Version Bump
*   Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 3.13-6
-   Mass removal python2
*   Wed Apr 08 2020 Tapas Kundu <tkundu@vmware.com> 3.13-5
-   Fix for CVE-2020-1747
*   Sat Mar 07 2020 Tapas Kundu <tkundu@vmware.com> 3.13-4
-   Fix for CVE-2019-20477
*   Tue Apr 16 2019 Tapas Kundu <tkundu@vmware.com> 3.13-3
-   Added lib3 changes for CVE-2017-18342
-   change default loader for yaml.add_constructor
-   Add custom constructors to multiple loaders
*   Thu Mar 28 2019 Ankit Jain <ankitja@vmware.com> 3.13-2
-   Fix for CVE-2017-18342
*   Thu Sep 20 2018 Tapas Kundu <tkundu@vmware.com> 3.13-1
-   Updated to release 3.13
*   Tue May 16 2017 Kumar Kaushik <kaushikk@vmware.com> 3.12-2
-   Adding python3 support.
*   Tue Apr 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.12-1
-   Updated version to 3.12
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.11-2
-   GA - Bump release of all rpms
*   Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
