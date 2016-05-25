Summary: Utility tools for control groups of Linux
Name: cgroup-utils
Version: 0.6
Release: 2%{?dist}
License: GPLv2
Group: Development/Libraries
URL: https://pypi.python.org/pypi/cgroup-utils/0.6

Source0: https://github.com/peo3/cgroup-utils/archive/%{name}-%{version}.tar.gz
%define sha1 cgroup-utils=c0c9c6ddcd7e5ce2eb04394aa1ad46e1b05eb669

BuildRequires:  python-setuptools
BuildRequires:  python2-devel

Requires: python2

%description
cgroup-utils provides utility tools and libraries for control groups of Linux. For example, 
cgutil top is a top-like tool which shows activities of running processes in control groups.

%prep
%setup -q

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=%{buildroot} --record=INSTALLED_FILES

%clean
%{__rm} -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6-2
-	GA - Bump release of all rpms
*	Wed Jan 6 2016 Xiaolin Li <xiaolinl@vmware.com> 0.6-1
-	Initial build.	First version