%define srcname docutils

Summary:        Docutils -- Python Documentation Utilities.
Name:           python3-docutils
Version:        0.16
Release:        3%{?dist}
License:        public domain, Python, 2-Clause BSD, GPL 3 (see COPYING.txt)
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/docutils

Source0: https://files.pythonhosted.org/packages/source/d/docutils/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=4e0c6662924cac6b8f28bb77a4f50eafd637c1083990a23dbd905d8a05362a18dae96e63408ed43b595b693ca755c7961d1282129d3215ed3774af0dddcc0466

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-lxml

Requires: python3
Requires: python3-lxml

BuildArch: noarch

%description
Docutils is a modular system for processing documentation into useful formats, such as HTML, XML, and LaTeX. For input Docutils supports reStructuredText, an easy-to-read, what-you-see-is-what-you-get plaintext markup syntax.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}
mv %{buildroot}%{_bindir}/rstpep2html.py %{buildroot}%{_bindir}/rstpep2html3.py
mv %{buildroot}%{_bindir}/rst2xml.py %{buildroot}%{_bindir}/rst2xml3.py
mv %{buildroot}%{_bindir}/rst2xetex.py %{buildroot}%{_bindir}/rst2xetex3.py
mv %{buildroot}%{_bindir}/rst2s5.py %{buildroot}%{_bindir}/rst2s53.py
mv %{buildroot}%{_bindir}/rst2pseudoxml.py %{buildroot}%{_bindir}/rst2pseudoxml3.py
mv %{buildroot}%{_bindir}/rst2odt_prepstyles.py %{buildroot}%{_bindir}/rst2odt_prepstyles3.py
mv %{buildroot}%{_bindir}/rst2odt.py %{buildroot}%{_bindir}/rst2odt3.py
mv %{buildroot}%{_bindir}/rst2man.py %{buildroot}%{_bindir}/rst2man3.py
mv %{buildroot}%{_bindir}/rst2latex.py %{buildroot}%{_bindir}/rst2latex3.py
mv %{buildroot}%{_bindir}/rst2html5.py %{buildroot}%{_bindir}/rst2html53.py
mv %{buildroot}%{_bindir}/rst2html.py %{buildroot}%{_bindir}/rst2html3.py

%if 0%{?with_check}
%check
PATH=%{buildroot}%{_bindir}:${PATH} \
  PYTHONPATH=%{buildroot}%{python3_sitelib}
%{python3} test3/alltests.py
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/rstpep2html3.py
%{_bindir}/rst2xml3.py
%{_bindir}/rst2xetex3.py
%{_bindir}/rst2s53.py
%{_bindir}/rst2pseudoxml3.py
%{_bindir}/rst2odt_prepstyles3.py
%{_bindir}/rst2odt3.py
%{_bindir}/rst2man3.py
%{_bindir}/rst2latex3.py
%{_bindir}/rst2html53.py
%{_bindir}/rst2html3.py
%{_bindir}/rst2html4.py

%changelog
* Tue Aug 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.16-3
- Add python3-lxml to requires
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.16-2
- Bump up to compile with python 3.10
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.16-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.14-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.14-1
- Update to version 0.14
* Thu Jun 22 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.13.1-3
- Add BuildRequires python-xml and python3-xml for the tests to pass
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.13.1-2
- Create separate packages for python2 and python3 in the bin directory
* Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 0.13.1-1
- Initial packaging for Photon
