Name:           PyYAML
Version:        3.12
Release:        1%{?dist}
Summary:        YAML parser and emitter for Python
Group:          Development/Libraries
License:        MIT
URL:            http://pyyaml.org/
Source0:        http://pyyaml.org/download/pyyaml/%{name}-%{version}.tar.gz
%define sha1 PyYAML=cb7fd3e58c129494ee86e41baedfec69eb7dafbe

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python2-devel
BuildRequires: libyaml-devel

Requires: python2
Requires: python2-libs
Requires: libyaml

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
%setup -q -n %{name}-%{version}

%build
%{__python} setup.py build
chmod a-x examples/yaml-highlight/yaml_hl.py

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%check
python setup.py test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc PKG-INFO README LICENSE examples
%{python_sitelib}/*


%changelog
*       Tue Apr 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.12-1
-       Updated version to 3.12
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.11-2
-	GA - Bump release of all rpms
* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
