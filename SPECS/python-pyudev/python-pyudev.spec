Summary:        Python binding for libudev
Name:           python3-pyudev
Version:        0.22.0
Release:        3%{?dist}
License:        GNU Library or Lesser General Public License (LGPL) (LGPL 2.1+)
Group:          Development/Languages/Python
URL:            https://pypi.org/project/pyudev
Source0:        pyudev-%{version}.tar.gz
%define         sha512 pyudev=a09ed479a54a1772a6af68cb975fef792068c2de3655e20223905bc3f574fd32bd3dbe6b97062eee3ab5f08a8b041ad3ea86dfb68c839ea44e29d65ec1686670
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-xml
BuildRequires:  systemd-devel
Requires:       systemd
Requires:       python3
Requires:       python3-six
%if 0%{?with_check}
BuildRequires:  python3-pip
BuildRequires:  curl-devel
BuildRequires:  python3-six
BuildRequires:  python3-py
BuildRequires:  python3-pytest
BuildRequires:  python3-attrs
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-docutils
%endif

%description
pyudev is a LGPL licensed, pure Python binding for libudev, the device and hardware management and information
library for Linux. It supports almost all libudev functionality. You can enumerate devices, query device properties and
attributes or monitor devices, including asynchronous monitoring with threads, or within the event loops of Qt, Glib
or wxPython.

The binding supports CPython 2 (2.6 or newer) and 3 (3.1 or newer), and PyPy 1.5 or newer. It is tested against udev
151 or newer, earlier versions of udev as found on dated Linux systems may work, but are not officially supported.

%prep
%autosetup -n pyudev-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
pip3 install pluggy more_itertools hypothesis mock
python3 setup.py test

%files
%defattr(-,root,root)
%doc COPYING README.rst
%{python3_sitelib}/*

%changelog
* Tue Feb 04 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.22.0-3
- Remove pip from Requires
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.22.0-2
- Bump up to compile with python 3.10
* Thu Mar 19 2020 Tapas Kundu <tkundu@vmware.com> 0.22.0-1
- Initial release.
