Name:           python3-ConcurrentLogHandler
Version:        0.9.23
Release:        1%{?dist}
Summary:        Concurrent logging handler (drop-in replacement for RotatingFileHandler) Python 2.6+
License:        Apache-2.0
Group:          Development/Languages/Python
Url:            https://pypi.org/project/concurrent-log-handler/
Source0:        https://files.pythonhosted.org/packages/15/b0/76d81143baf5bd320b6d976a30d401375f2b170efe99d4adc261ae5a6a90/concurrent-log-handler-0.9.23.tar.gz
%define sha512  concurrent-log-handler=4bda96499730d0c24587a3242d93c3074ed48b3373517e2b25d6795d86035bcf0f3472b771150454328275096bfbe70b3d86046587e7a5c930b25266f616dcdc
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif
Requires:       python3
Requires:       python3-setuptools
Requires:       python3-portalocker

BuildArch:      noarch

%description
ConcurrentLogHandler is a module that provides an additional log handler for Python’s standard logging package (PEP 282). This handler will write log events to log file which is rotated when the log file reaches a certain size. Multiple processes can safely write to the same log file concurrently.

%prep
%autosetup -n concurrent-log-handler-%{version}

%build
%{py3_build}

%install
%{py3_install}

%check
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
python3 stresstest.py

%files
%{python3_sitelib}/*

%changelog
* Mon May 01 2023 Prashant S Chauhan <psinghchauha@vmware.com> 0.9.23-1
- Update to compile with latest python & setuptools
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.9.1-6
- Bump up to compile with python 3.10
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.9.1-5
- Fix build with new rpm
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 0.9.1-4
- Mass removal python2
* Mon Dec 03 2018 Ashwin H <ashwinh@vmware.com> 0.9.1-3
- Add %check
* Thu Sep 21 2017 Bo Gan <ganb@vmware.com> 0.9.1-2
- Disable test as no tests are available
* Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.9.1-1
- Initial version of python-ConcurrentLogHandler package for Photon.
