%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:        A high-level cross-protocol url-grabber
Name:           urlgrabber
Version:        3.10.1
Release:        3%{?dist}
Source0:        urlgrabber-%{version}.tar.gz
%define sha1 urlgrabber=75206abe4c2498d4ff01498e4a35192a65c92f3e
License:        LGPLv2+
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:      noarch
Url:            http://urlgrabber.baseurl.org/
Vendor:         VMware, Inc.
Distribution:   Photon
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
*   Thu May 25 2017 Xiaolin Li <xiaolinl@vmware.com> 3.10.1-3
-   Added pycurl to requires.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.10.1-2
-   GA - Bump release of all rpms
*   Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 3.10.1-1
-   Upgrade version.
*   Sat Jan 24 2015 Touseef Liaqat <tliaqat@vmware.com> 3.10-1
-   Initial build.  First version
