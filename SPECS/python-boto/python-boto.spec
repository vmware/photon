%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Summary:        Amazon Web Services Library.
Name:           python-boto
Version:        2.49.0
Release:        1%{?dist}
License:        MIT License
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.python.org/pypi/boto/2.48.0
Source0:        https://files.pythonhosted.org/packages/source/b/boto/boto-%{version}.tar.gz
%define sha1    boto=300e6b7abd04a77a94f769e6cad6fb9e6e84ffbb
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-six
BuildRequires:  python-xml
%if %{with_check}
BuildRequires:  python-requests
%endif
Requires:       python2
Requires:       python2-libs
Requires:       python-requests
Requires:       python-xml
BuildArch:      noarch

%description
Boto is a Python package that provides interfaces to Amazon Web Services. Currently, all features work with Python 2.6 and 2.7. Work is under way to support Python 3.3+ in the same codebase. Modules are being ported one at a time with the help of the open source community, so please check below for compatibility with Python 3.3+.

%package -n     python3-boto
Summary:        python-boto
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python3-requests
%endif
Requires:       python3
Requires:       python3-libs
Requires:       python3-requests
Requires:       python3-xml

%description -n python3-boto
Python 3 version.

%prep
%setup -q -n boto-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}
for item in %{buildroot}/%{_bindir}/*
    do mv ${item} "${item}-%{python3_version}" ;
done
popd
python2 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}

%check
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 nose
$easy_install_2 httpretty
$easy_install_2 mock
python2 ./tests/test.py unit

pushd ../p3dir
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 nose
$easy_install_3 httpretty
$easy_install_3 mock
python3 ./tests/test.py unit
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*
%{_bindir}/asadmin
%{_bindir}/bundle_image
%{_bindir}/cfadmin
%{_bindir}/cq
%{_bindir}/cwutil
%{_bindir}/dynamodb_dump
%{_bindir}/dynamodb_load
%{_bindir}/elbadmin
%{_bindir}/fetch_file
%{_bindir}/glacier
%{_bindir}/instance_events
%{_bindir}/kill_instance
%{_bindir}/launch_instance
%{_bindir}/list_instances
%{_bindir}/lss3
%{_bindir}/mturk
%{_bindir}/pyami_sendmail
%{_bindir}/route53
%{_bindir}/s3put
%{_bindir}/sdbadmin
%{_bindir}/taskadmin

%files -n python3-boto
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/asadmin-%{python3_version}
%{_bindir}/bundle_image-%{python3_version}
%{_bindir}/cfadmin-%{python3_version}
%{_bindir}/cq-%{python3_version}
%{_bindir}/cwutil-%{python3_version}
%{_bindir}/dynamodb_dump-%{python3_version}
%{_bindir}/dynamodb_load-%{python3_version}
%{_bindir}/elbadmin-%{python3_version}
%{_bindir}/fetch_file-%{python3_version}
%{_bindir}/glacier-%{python3_version}
%{_bindir}/instance_events-%{python3_version}
%{_bindir}/kill_instance-%{python3_version}
%{_bindir}/launch_instance-%{python3_version}
%{_bindir}/list_instances-%{python3_version}
%{_bindir}/lss3-%{python3_version}
%{_bindir}/mturk-%{python3_version}
%{_bindir}/pyami_sendmail-%{python3_version}
%{_bindir}/route53-%{python3_version}
%{_bindir}/s3put-%{python3_version}
%{_bindir}/sdbadmin-%{python3_version}
%{_bindir}/taskadmin-%{python3_version}

%changelog
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.49.0-1
-   Update to version 2.49.0
*   Tue Sep 12 2017 Xiaolin Li <xiaolinl@vmware.com> 2.48.0-1
-   Initial packaging for Photon
