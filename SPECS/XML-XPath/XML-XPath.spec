Summary:        XML-XPath perl module
Name:           XML-XPath
Version:        1.37
Release:        1%{?dist}
License:        GPL+
URL:            http://search.cpan.org/~toddr/%{name}-%{version}/
Source0:        https://cpan.metacpan.org/authors/id/M/MA/MANWAR/%{name}-%{version}.tar.gz
%define sha1 XML-XPath=8cedbb3073e064f6c827697aad5539f26147a4f5
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
*   Tue Sep 6 2016 Xiaolin Li <xiaolinl@vmware.com> 1.37-1
-   Initial build. First version
