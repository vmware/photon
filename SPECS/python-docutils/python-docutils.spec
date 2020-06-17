%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Docutils -- Python Documentation Utilities.
Name:           python3-docutils
Version:        0.14
Release:        2%{?dist}
License:        public domain, Python, 2-Clause BSD, GPL 3 (see COPYING.txt)
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/docutils
Source0:        https://files.pythonhosted.org/packages/source/d/docutils/docutils-%{version}.tar.gz
%define sha1    docutils=32cefb69ac3dab5b04c4d150776f35419cc4c863

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
Docutils is a modular system for processing documentation into useful formats, such as HTML, XML, and LaTeX. For input Docutils supports reStructuredText, an easy-to-read, what-you-see-is-what-you-get plaintext markup syntax.


%prep
%setup -q -n docutils-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/rstpep2html.py %{buildroot}/%{_bindir}/rstpep2html3.py
mv %{buildroot}/%{_bindir}/rst2xml.py %{buildroot}/%{_bindir}/rst2xml3.py
mv %{buildroot}/%{_bindir}/rst2xetex.py %{buildroot}/%{_bindir}/rst2xetex3.py
mv %{buildroot}/%{_bindir}/rst2s5.py %{buildroot}/%{_bindir}/rst2s53.py
mv %{buildroot}/%{_bindir}/rst2pseudoxml.py %{buildroot}/%{_bindir}/rst2pseudoxml3.py
mv %{buildroot}/%{_bindir}/rst2odt_prepstyles.py %{buildroot}/%{_bindir}/rst2odt_prepstyles3.py
mv %{buildroot}/%{_bindir}/rst2odt.py %{buildroot}/%{_bindir}/rst2odt3.py
mv %{buildroot}/%{_bindir}/rst2man.py %{buildroot}/%{_bindir}/rst2man3.py
mv %{buildroot}/%{_bindir}/rst2latex.py %{buildroot}/%{_bindir}/rst2latex3.py
mv %{buildroot}/%{_bindir}/rst2html5.py %{buildroot}/%{_bindir}/rst2html53.py
mv %{buildroot}/%{_bindir}/rst2html.py %{buildroot}/%{_bindir}/rst2html3.py

%check
PATH=%{buildroot}%{_bindir}:${PATH} \
  PYTHONPATH=%{buildroot}%{python3_sitelib}
python3 test3/alltests.py

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
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.14-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.14-1
-   Update to version 0.14
*   Thu Jun 22 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.13.1-3
-   Add BuildRequires python-xml and python3-xml for the tests to pass
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.13.1-2
-   Create separate packages for python2 and python3 in the bin directory
*   Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 0.13.1-1
-   Initial packaging for Photon
