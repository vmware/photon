%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:		A high-level cross-protocol url-grabber
Name: 			urlgrabber
Version: 		3.10
Release: 		1%{?dist}
Source0: 		urlgrabber-%{version}.tar.gz
%define sha1 urlgrabber=a2ff4fc2056f4d91b412104e04ff0bdc73ec5fb1
License: 		LGPLv2+
Group: 			Development/Libraries
BuildRoot: 		%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: 		noarch
Url: 			http://linux.duke.edu/projects/urlgrabber/
Vendor:			VMware, Inc.
Distribution:		Photon
Provides: 		urlgrabber = %{version}-%{release}
BuildRequires:  	pycurl
BuildRequires:		python2
BuildRequires:		python2-libs
Requires:		python2
Requires:		curl

%description
A high-level cross-protocol url-grabber for python supporting HTTP, FTP 
and file locations.  Features include keepalive, byte ranges, throttling,
authentication, proxies and more.

%prep
%setup -q -n urlgrabber-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install -O1 --root=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{_docdir}/urlgrabber-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE README TODO
%{python_sitelib}/urlgrabber*
%{_bindir}/urlgrabber
%dir /usr/libexec
%attr(0755,root,root) /usr/libexec/urlgrabber-ext-down

%changelog
*	Sat Jan 24 2015 Touseef Liaqat <tliaqat@vmware.com> 3.10
-	Initial build.	First version
