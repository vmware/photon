Summary:        Python-PostgreSQL Database Adapter
Name:           python3-psycopg2
Version:        2.7.5
Release:        3%{?dist}
Url:            https://pypi.python.org/pypi/psycopg2
License:        LGPL with exceptions or ZPL
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/source/p/psycopg2/psycopg2-%{version}.tar.gz
%define sha512 psycopg2=5bf85b6760871f904b6b570ea454f99b72cf97acf9cce10b63dc7b6b0b18913b50ad4f24c469d101c54de6ad6100f1cac3c58225076b5e584a677f5ab4170a93

BuildRequires:  python3-setuptools
BuildRequires:  postgresql10-devel
BuildRequires:  python3-devel

%if 0%{?with_check}
BuildRequires: shadow
BuildRequires: sudo
%endif

Requires:       python3
Requires:       (postgresql10-libs >= 10.5 or postgresql13-libs)

%description
Psycopg is the most popular PostgreSQL database adapter for the Python programming language. Its main features are the complete implementation of the Python DB API 2.0 specification and the thread safety (several threads can share the same connection). It was designed for heavily multi-threaded applications that create and destroy lots of cursors and make a large number of concurrent “INSERT”s or “UPDATE”s.

Psycopg 2 is mostly implemented in C as a libpq wrapper, resulting in being both efficient and secure. It features client-side and server-side cursors, asynchronous communication and notifications, “COPY TO/COPY FROM” support. Many Python types are supported out-of-the-box and adapted to matching PostgreSQL data types; adaptation can be extended and customized thanks to a flexible objects adaptation system.

Psycopg 2 is both Unicode and Python 3 friendly.

%prep
%autosetup -p1 -n psycopg2-%{version}

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
* Fri Nov 18 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.7.5-3
- Require psql or psql13
- Remove python2 variant of this package
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
