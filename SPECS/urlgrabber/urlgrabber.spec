%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:        A high-level cross-protocol url-grabber
Name:           urlgrabber
Version:        3.10.2
Release:        4%{?dist}
License:        LGPLv2+
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://urlgrabber.baseurl.org/
Source0:        urlgrabber-%{version}.tar.gz
%define sha1    urlgrabber=6061ca1fc4e1557e3c578ec76c1621a4f6d9747c

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:      noarch

Provides:       urlgrabber = %{version}-%{release}
BuildRequires:  pycurl
BuildRequires:  python2
BuildRequires:  python2-libs
Requires:       python2
Requires:       curl
Requires:       pycurl

%description
A high-level cross-protocol url-grabber for python supporting HTTP, FTP 
and file locations.  Features include keepalive, byte ranges, throttling,
authentication, proxies and more.

%prep
%setup -q -n urlgrabber-%{version}

%build
python2 setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python2 setup.py install -O1 --root=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{_docdir}/urlgrabber-%{version}

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE README TODO
%{python2_sitelib}/urlgrabber*
%{_bindir}/urlgrabber
%dir /usr/libexec
%attr(0755,root,root) /usr/libexec/urlgrabber-ext-down

%changelog
*   Thu Jun 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.10.2-4
-   Use python2 explicitly to build
*   Tue Jun 05 2017 Chang Lee <changlee@vmware.com> 3.10.2-3
-   Remove thread option in %check
*   Thu May 25 2017 Xiaolin Li <xiaolinl@vmware.com> 3.10.2-2
-   Added pycurl to requires.
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 3.10.2-1
-   Updated to version 3.10.2.
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 3.10.1-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.10.1-2
-   GA - Bump release of all rpms
*   Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 3.10.1-1
-   Upgrade version.
*   Sat Jan 24 2015 Touseef Liaqat <tliaqat@vmware.com> 3.10-1
-   Initial build.  First version
