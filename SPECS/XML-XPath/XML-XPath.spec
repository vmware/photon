Summary:        XML-XPath perl module
Name:           XML-XPath
Version:        1.40
Release:        1%{?dist}
License:        GPL+
URL:            http://search.cpan.org/~toddr/%{name}-%{version}/
Source0:        https://cpan.metacpan.org/authors/id/M/MA/MANWAR/%{name}-%{version}.tar.gz
%define sha1 XML-XPath=a373c9d071a6c675c77320a905053baa5e7a99ff
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  XML-Parser
%description
This module aims to comply exactly to the XPath specification at http://www.w3.org/TR/xpath and yet allow extensions to be added in the form of functions. Modules such as XSLT and XPointer may need to do this as they support functionality beyond XPath.
%prep
%setup -q
%build
perl Makefile.PL --prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} -k test

%files
%defattr(-,root,root)
%{_bindir}/xpath
%{_libdir}/perl5/*
%{_mandir}/man3/*
%{_mandir}/man1/*
%changelog
*   Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 1.40-1
-   Version update
*   Tue Sep 6 2016 Xiaolin Li <xiaolinl@vmware.com> 1.37-1
-   Initial build. First version
