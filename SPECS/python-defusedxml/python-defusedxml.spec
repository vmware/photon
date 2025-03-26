
Summary:        XML bomb protection for Python stdlib modules
Name:           python3-defusedxml
Version:        0.7.1
Release:        3%{?dist}
Url:            https://pypi.python.org/pypi/defusedxml
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        defusedxml-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
Requires:       python3-xml

%description
The results of an attack on a vulnerable XML library can be fairly dramatic. With just a few hundred Bytes of XML data an attacker can occupy several Gigabytes of memory within seconds. An attacker can also keep CPUs busy for a long time with a small to medium size request. Under some circumstances it is even possible to access local files on your server, to circumvent a firewall, or to abuse services to rebound attacks to third parties.

The attacks use and abuse less common features of XML and its parsers. The majority of developers are unacquainted with features such as processing instructions and entity expansions that XML inherited from SGML. At best they know about <!DOCTYPE> from experience with HTML but they are not aware that a document type definition (DTD) can generate an HTTP request or load a file from the file system.

None of the issues is new. They have been known for a long time. Billion laughs was first reported in 2003. Nevertheless some XML libraries and applications are still vulnerable and even heavy users of XML are surprised by these features. It's hard to say whom to blame for the situation. It's too short sighted to shift all blame on XML parsers and XML libraries for using insecure default settings. After all they properly implement XML specifications. Application developers must not rely that a library is always configured for security and potential harmful data by default.

%prep
%autosetup -n defusedxml-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.7.1-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.7.1-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.7.1-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.6.0-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.5.0-4
- Mass removal python2
* Tue Aug 01 2017 Xiaolin Li <xiaolinl@vmware.com> 0.5.0-3
- Added python-xml to requires of python-defusedxml.
- Added python3-xml to requires of python3-defusedxml.
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.5.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Mar 09 2017 Xiaolin Li <xiaolinl@vmware.com> 0.5.0-1
- Initial packaging for Photon
