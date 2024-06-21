%define srcname     psycopg2

Summary:        Python-PostgreSQL Database Adapter
Name:           python3-psycopg2
Version:        2.8.6
Release:        5%{?dist}
Url:            https://pypi.python.org/pypi/psycopg2
License:        LGPL with exceptions or ZPL
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/source/p/psycopg2/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=1e1d5d8755c6d1a153d84210bf29902afafe853659d709e13abc6bc5772def13779d2394690af1c544384c9c607edc0fe5cf2763244fb346febf9a9e0032b45f

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  postgresql15-devel

%if 0%{?with_check}
BuildRequires: shadow
BuildRequires: sudo
%endif

Requires:       python3
Requires:       (postgresql15-libs or postgresql14-libs or postgresql13-libs or postgresql10-libs)

%description
Psycopg is the most popular PostgreSQL database adapter for the Python programming language. Its main features are the complete implementation of the Python DB API 2.0 specification and the thread safety (several threads can share the same connection). It was designed for heavily multi-threaded applications that create and destroy lots of cursors and make a large number of concurrent “INSERT”s or “UPDATE”s.

Psycopg 2 is mostly implemented in C as a libpq wrapper, resulting in being both efficient and secure. It features client-side and server-side cursors, asynchronous communication and notifications, “COPY TO/COPY FROM” support. Many Python types are supported out-of-the-box and adapted to matching PostgreSQL data types; adaptation can be extended and customized thanks to a flexible objects adaptation system.

Psycopg 2 is both Unicode and Python 3 friendly.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
%define user postgres
%define data_dir "/home/%{user}/data"
chmod 700 /etc/sudoers
echo 'Defaults env_keep += "PYTHONPATH"' >> /etc/sudoers
#start postgresql server and create a database named psycopg2_test
useradd -m %{user}
groupadd -f %{user}
rm -rf %{data_dir}
mkdir -p %{data_dir}
chown %{user}:%{user} %{data_dir}
chmod 700 %{data_dir}
su - %{user} -c 'initdb -D %{data_dir}'
cat <<EOT >> %{data_dir}/postgresql.conf
client_encoding = 'UTF8'
unix_socket_directories = '/run/postgresql'
EOT
mkdir -p /run/postgresql
chown -R %{user}:%{user} /run/postgresql
su - %{user} -c 'pg_ctl -D %{data_dir} -l logfile start'
sleep 3
su - %{user} -c 'createdb psycopg2_test'
export PYTHONPATH=${PYTHONPATH}:%{buildroot}%{python3_sitelib}
sudo -u %{user} python3 -c "from psycopg2 import tests; tests.unittest.main(defaultTest='tests.test_suite')" --verbose
su - %{user} -c 'pg_ctl -D %{data_dir} stop'
rm -rf %{data_dir}
userdel -rf %{user}
groupdel -f %{user}
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Jun 19 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 2.8.6-5
- Build with pgsql15
* Fri Dec 09 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.8.6-4
- Fix pgsql requires
* Fri Dec 10 2021 Tapas Kundu <tkundu@vmware.com> 2.8.6-3
- Bump up to build with postgresql 14.1
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.8.6-2
- Bump up to compile with python 3.10
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
