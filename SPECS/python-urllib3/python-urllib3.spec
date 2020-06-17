%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A powerful, sanity-friendly HTTP client for Python.
Name:           python3-urllib3
Version:        1.23
Release:        3%{?dist}
Url:            https://pypi.python.org/pypi/urllib3
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/shazow/urllib3/archive/urllib3-%{version}.tar.gz
%define sha1    urllib3=0c54209c397958a7cebe13cb453ec8ef5833998d

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
#%if %{with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python3-pip
#%endif

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
urllib3 is a powerful, sanity-friendly HTTP client for Python. Much of the Python ecosystem already uses urllib3 and you should too.


%prep
%setup -q -n urllib3-%{version}
# Dummyserver tests are failing when running in chroot. So disabling the tests.
rm -rf test/with_dummyserver/

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check

nofiles=$(ulimit -n)
ulimit -n 5000
pip3 install -r dev-requirements.txt

ignoretestslist='not test_select_interrupt_exception and not test_selector_error and not timeout and not test_request_host_header_ignores_fqdn_dot and not test_dotted_fqdn'
case $(uname -m) in
ppc*)
ignoretestslist="$ignoretestslist and not test_select_timing and not test_select_multiple_interrupts_with_event and not test_interrupt_wait_for_read_with_event and not test_select_interrupt_with_event";;
esac

PYTHONPATH="%{buildroot}%{$python3_sitelib}" pytest \
                --ignore=test/appengine \
                --ignore=test/with_dummyserver/test_proxy_poolmanager.py \
                --ignore=test/with_dummyserver/test_poolmanager.py \
                --ignore=test/contrib/test_pyopenssl.py \
                --ignore=test/contrib/test_securetransport.py \
                -k "${ignoretestslist}" \
                urllib3 test
ulimit -n $nofiles


%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 1.23-3
-   Mass removal python2
*   Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> 1.23-2
-   Fix make check
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.23-1
-   Update to version 1.23
*   Tue Aug 15 2017 Xiaolin Li <xiaolinl@vmware.com> 1.20-5
-   Increased number of open files per process to 5000 before run make check.
*   Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> 1.20-4
-   Fixed rpm check errors
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.20-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.20-2
-   Use python2 explicitly
*   Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.20-1
-   Initial packaging for Photon
