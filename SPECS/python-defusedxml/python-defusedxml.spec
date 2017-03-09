%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        XML bomb protection for Python stdlib modules
Name:           python-defusedxml
Version:        0.5.0
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/defusedxml
License:        PSFL
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        defusedxml-%{version}.tar.gz
%define sha1    defusedxml=70ff80a849bbc2e9241daa1debda9f43e7fbdff0

BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

%description
The results of an attack on a vulnerable XML library can be fairly dramatic. With just a few hundred Bytes of XML data an attacker can occupy several Gigabytes of memory within seconds. An attacker can also keep CPUs busy for a long time with a small to medium size request. Under some circumstances it is even possible to access local files on your server, to circumvent a firewall, or to abuse services to rebound attacks to third parties.

The attacks use and abuse less common features of XML and its parsers. The majority of developers are unacquainted with features such as processing instructions and entity expansions that XML inherited from SGML. At best they know about <!DOCTYPE> from experience with HTML but they are not aware that a document type definition (DTD) can generate an HTTP request or load a file from the file system.

None of the issues is new. They have been known for a long time. Billion laughs was first reported in 2003. Nevertheless some XML libraries and applications are still vulnerable and even heavy users of XML are surprised by these features. It's hard to say whom to blame for the situation. It's too short sighted to shift all blame on XML parsers and XML libraries for using insecure default settings. After all they properly implement XML specifications. Application developers must not rely that a library is always configured for security and potential harmful data by default.

%package -n     python3-defusedxml
Summary:        python-defusedxml
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description -n python3-defusedxml

Python 3 version.

%prep
%setup -q -n defusedxml-%{version}
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

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-defusedxml
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Thu Mar 09 2017 Xiaolin Li <xiaolinl@vmware.com> 0.5.0-1
-   Initial packaging for Photon
