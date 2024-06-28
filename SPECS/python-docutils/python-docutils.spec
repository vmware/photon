%define srcname docutils

Summary:        Docutils -- Python Documentation Utilities.
Name:           python3-docutils
Version:        0.19
Release:        2%{?dist}
License:        public domain, Python, 2-Clause BSD, GPL 3 (see COPYING.txt)
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/docutils

Source0: https://files.pythonhosted.org/packages/source/d/docutils/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=fb904a899f2b6f3c07c5079577bd7c52a3182cb85f6a4149391e523498df15bfa317f0c04095b890beeb3f89c2b444875a2a609d880ac4d7fbc3125e46b37ea5

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

%if 0%{?with_check}
%check
PATH=%{buildroot}%{_bindir}:${PATH} \
  PYTHONPATH=%{buildroot}%{python3_sitelib}
%{python3} test/alltests.py
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/%{srcname}
%{_bindir}/rstpep2html.py
%{_bindir}/rst2xml.py
%{_bindir}/rst2xetex.py
%{_bindir}/rst2s5.py
%{_bindir}/rst2pseudoxml.py
%{_bindir}/rst2odt_prepstyles.py
%{_bindir}/rst2odt.py
%{_bindir}/rst2man.py
%{_bindir}/rst2latex.py
%{_bindir}/rst2html5.py
%{_bindir}/rst2html.py
%{_bindir}/rst2html4.py

%changelog
* Tue Aug 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.19-2
- Add python3-lxml to requires
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.19-1
- Automatic Version Bump
* Tue Mar 15 2022 Nitesh Kumar <kunitesh@vmware.com> 0.16-2
- Version bump up, required by bluez 5.63
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
