Summary:        Python-PostgreSQL Database Adapter
Name:           python3-psycopg2
Version:        2.9.3
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/psycopg2
License:        LGPL with exceptions or ZPL
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/p/psycopg2/psycopg2-%{version}.tar.gz
%define sha512  psycopg2=048184d1d162a371fc0fba711448a6fa8a6aac193421f4484c7f7b91c39065d5b632fa34fc15a901eca055d597302b1f9e38330b248ed0e4653dcdc544b0d660

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  postgresql-devel >= 10.5
Requires:       python3
Requires:       python3-libs
Requires:       postgresql >= 10.5

%description
Psycopg is the most popular PostgreSQL database adapter for the Python programming language. Its main features are the complete implementation of the Python DB API 2.0 specification and the thread safety (several threads can share the same connection). It was designed for heavily multi-threaded applications that create and destroy lots of cursors and make a large number of concurrent “INSERT”s or “UPDATE”s.

Psycopg 2 is mostly implemented in C as a libpq wrapper, resulting in being both efficient and secure. It features client-side and server-side cursors, asynchronous communication and notifications, “COPY TO/COPY FROM” support. Many Python types are supported out-of-the-box and adapted to matching PostgreSQL data types; adaptation can be extended and customized thanks to a flexible objects adaptation system.

Psycopg 2 is both Unicode and Python 3 friendly.

%prep
%autosetup -n psycopg2-%{version}

%build
%py3_build

%install
%py3_install

%check
chmod 700 /etc/sudoers
echo 'Defaults env_keep += "PYTHONPATH"' >> /etc/sudoers
#start postgresql server and create a database named psycopg2_test
useradd -m postgres &>/dev/null
groupadd postgres &>/dev/null
rm -r /home/postgres/data &>/dev/null ||:
mkdir -p /home/postgres/data
chown postgres:postgres /home/postgres/data
chmod 700 /home/postgres/data
su - postgres -c 'initdb -D /home/postgres/data'
echo "client_encoding = 'UTF8'" >> /home/postgres/data/postgresql.conf
echo "unix_socket_directories = '/run/postgresql'" >> /home/postgres/data/postgresql.conf
mkdir -p /run/postgresql
chown -R postgres:postgres /run/postgresql
su - postgres -c 'pg_ctl -D /home/postgres/data -l logfile start'
sleep 3
su - postgres -c 'createdb psycopg2_test'
PYTHONPATH=%{buildroot}%{python3_sitelib} PATH=$PATH:%{buildroot}%{_bindir} sudo -u postgres python3 -c "from psycopg2 import tests; tests.unittest.main(defaultTest='tests.test_suite')" --verbose
su - postgres -c 'pg_ctl -D /home/postgres/data stop'
rm -r /home/postgres/data &>/dev/null ||:

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.9.3-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.9.3-1
- Automatic Version Bump
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 2.8.6-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.8.5-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 2.7.5-3
- Mass removal python2
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 2.7.5-2
- Consuming postgresql 10.5 version
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.7.5-1
- Update to version 2.7.5
* Wed Aug 09 2017 Xiaolin Li <xiaolinl@vmware.com> 2.7.1-3
- Fixed make check errors
* Thu Jul 6 2017 Divya Thaluru <dthaluru@vmware.com> 2.7.1-2
- Added build requires on postgresql-devel
* Wed Apr 26 2017 Xialin Li <xiaolinl@vmware.com> 2.7.1-1
- Initial packaging for Photon
