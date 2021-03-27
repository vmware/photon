%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Name:           python3-pip
Version:        21.0.1
Release:        3%{?dist}
Url:            https://pypi.python.org/pypi/pip
Summary:        The PyPA recommended tool for installing Python packages.
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/11/b6/abcb525026a4be042b486df43905d6893fb04f05aac21c32c638e939e447/pip-%{version}.tar.gz
%define sha1    pip=f74aa5460852ab99f4433212af87949168a8181c
# To get tests:
# git clone https://github.com/pypa/pip && cd pip
# git checkout 9.0.1 && tar -czvf ../pip-tests-9.0.1.tar.gz tests/
Source1:        pip-tests-%{version}.tar.gz
%define sha1 pip-tests=7a2a0eb406a8c27fd4961164ace46dc28e0cb216
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools
Requires:       python3-xml
BuildArch:      noarch

%description
The PyPA recommended tool for installing Python packages.


%prep
%setup -q -n pip-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check

%files
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/*
%exclude %{_bindir}/pip
%exclude %{python3_sitelib}/pip/_vendor/distlib/*.exe
#excluded packaging pip as its conflicting with python2 pip.
#also previous python3-pip was providing pip3 and not pip

%changelog
*   Sat Mar 27 2021 Tapas Kundu <tkundu@vmware.com> 21.0.1-3
-   Do not package exe file
*   Fri Mar 26 2021 Piyush Gupta <gpiyush@vmware.com> 21.0.1-2
-   Added source name for pip-tests
*   Tue Feb 16 2021 Tapas Kundu <tkundu@vmware.com> 21.0.1-1
-   Updating pip3 to 21.0.1
