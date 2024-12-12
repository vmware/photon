Summary:          A password strength-checking library.
Name:             cracklib
Version:          2.9.8
Release:          3%{?dist}
Group:            System Environment/Libraries
URL:              https://github.com/cracklib/cracklib
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: https://github.com/cracklib/cracklib/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}-%{version}=03b97e3ab3bd73e4a5673254622d542e5ad5cae642183afe1c84f17b174284a0d618de71aa09e858b924018665bc5107cedaaa73ae2e289c0b0d1d89eed618e7

Source1: https://github.com/cracklib/cracklib/releases/download/v%{version}/%{name}-words-%{version}.gz
%define sha512  %{name}-words-%{version}=1700c56b9776b7ae4684b9ab1e784dd7707550bce2149301f662618a4f00a2eb0ba2d1a206c09aac22f7d95bc561544d412d2fdac5008fc3aabc4872e8a74afc

Source2: license.txt
%include %{SOURCE2}

BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-xml

# cross compilation requires native dicts generating tools
%define BuildRequiresNative %{name}-dicts

Requires:         /usr/bin/ln
Requires(post):   /usr/bin/ln
Requires(postun): /usr/bin/rm

%description
CrackLib tests passwords to determine whether they match certain
security-oriented characteristics. You can use CrackLib to stop
users from choosing passwords which would be easy to guess. CrackLib
performs certain tests:

* It tries to generate words from a username and gecos entry and
  checks those words against the password;
* It checks for simplistic patterns in passwords;
* It checks for the password in a dictionary.

CrackLib is actually a library containing a particular
C function which is used to check the password, as well as
other C functions. CrackLib is not a replacement for a passwd
program; it must be used in conjunction with an existing passwd
program.

Install the cracklib package if you need a program to check users'
passwords to see if they are at least minimally secure. If you
install CrackLib, you'll also want to install the cracklib-dicts
package.

%package    dicts
Summary:    The standard CrackLib dictionaries.
Group:      System Environment/Utilities
Requires:   %{name} = %{version}-%{release}

%description    dicts
The cracklib-dicts package includes the CrackLib dictionaries.
CrackLib will need to use the dictionary appropriate to your system,
which is normally put in /usr/share/dict/words.  Cracklib-dicts also contains
the utilities necessary for the creation of new dictionaries.

If you are installing CrackLib, you should also install cracklib-dicts.

%package devel
Summary:    Cracklib link library & header file
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
The cracklib devel package include the needed library link and
header files for development.

%package -n python3-%{name}
Summary:    The cracklib python module
Group:      Development/Languages/Python
Requires:   %{name} = %{version}-%{release}
Requires:   python3
Requires:   python3-libs

%description -n python3-%{name}
The cracklib python3 module

%package lang
Summary:    The CrackLib language pack.
Group:      System Environment/Libraries

%description lang
The CrackLib language pack.

%prep
%autosetup -p1 -n %{name}-%{version}
chmod -R og+rX .
mkdir -p src/dicts
install %{SOURCE1} src/dicts/

%build
if [ %{_host} != %{_build} ]; then
  export PYTHONXCPREFIX=/target-%{_arch}/usr
  export CC=%{_host}-gcc
  export LDSHARED='%{_host}-gcc -shared'
  export LDFLAGS='-L/target-%{_arch}/usr/lib'
fi

export CFLAGS="%{optflags}"

pushd src

./autogen.sh

%configure \
  --disable-static \
  --without-python

%make_build

pushd python
%py3_build
popd
popd

%install
pushd src
%make_install %{?_smp_mflags}
rm -f %{buildroot}%{_libdir}/*.la

chmod 755 ./util/%{name}-format \
          ./util/%{name}-packer

if [ %{_host} = %{_build} ]; then
  export PATH=./util:$PATH
fi

%{name}-format dicts/%{name}* | %{name}-packer %{buildroot}%{_datadir}/%{name}/words
echo password | %{name}-packer %{buildroot}%{_datadir}/%{name}/empty
rm -f %{buildroot}%{_datadir}/%{name}/%{name}-small
ln -sv %{name}-format %{buildroot}%{_sbindir}/mkdict
ln -sv %{name}-packer %{buildroot}%{_sbindir}/packer

pushd python
%py3_install
popd
popd

%if 0%{?with_check}
%check
mkdir -p %{_datadir}/%{name}
cp %{buildroot}%{_datadir}/%{name}/* %{_datadir}/%{name}/
make %{?_smp_mflags} test
%endif

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
[ $1 = 1 ] || exit 0
echo "using empty dict to provide pw_dict" >&2
ln -sf empty.hwm %{_datadir}/%{name}/pw_dict.hwm
ln -sf empty.pwd %{_datadir}/%{name}/pw_dict.pwd
ln -sf empty.pwi %{_datadir}/%{name}/pw_dict.pwi

%triggerin -- %{name}-dicts
[ $2 = 1 ] || exit 0
echo "switching pw_dict to cracklib-dicts" >&2
ln -sf words.hwm %{_datadir}/%{name}/pw_dict.hwm
ln -sf words.pwd %{_datadir}/%{name}/pw_dict.pwd
ln -sf words.pwi %{_datadir}/%{name}/pw_dict.pwi

%triggerun -- %{name}-dicts
[ $2 = 0 ] || exit 0
echo "switching pw_dict to empty dict" >&2
ln -sf empty.hwm %{_datadir}/%{name}/pw_dict.hwm
ln -sf empty.pwd %{_datadir}/%{name}/pw_dict.pwd
ln -sf empty.pwi %{_datadir}/%{name}/pw_dict.pwi

%postun
/sbin/ldconfig
[ $1 = 0 ] || exit 0
rm -f %{_datadir}/%{name}/pw_dict.hwm \
      %{_datadir}/%{name}/pw_dict.pwd \
      %{_datadir}/%{name}/pw_dict.pwi

%files
%defattr(-,root,root)
%{_datadir}/%{name}/%{name}.magic
%{_datadir}/%{name}/empty*
%{_libdir}/libcrack.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libcrack.so

%files -n python3-%{name}
%defattr(-,root,root)
%{python3_sitelib}/*

%files dicts
%defattr(-,root,root)
%{_sbindir}/*
%{_datadir}/%{name}/words*

%files lang
%defattr(-,root,root)
%{_datadir}/locale/*

%changelog
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 2.9.8-3
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.9.8-2
- Release bump for SRP compliance
* Mon Oct 31 2022 Gerrit Photon <photon-checkins@vmware.com> 2.9.8-1
- Automatic Version Bump
* Mon Aug 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.9.7-2
- Remove .la files
* Tue Jul 21 2020 Gerrit Photon <photon-checkins@vmware.com> 2.9.7-1
- Automatic Version Bump
* Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 2.9.6-10
- Mass removal python2
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 2.9.6-9
- Cross compilation support
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.9.6-8
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Sun Jun 04 2017 Bo Gan <ganb@vmware.com> 2.9.6-7
- Fix script dependency
* Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> 2.9.6-6
- Move python2 requires to python subpackage and added python3.
* Thu Apr 13 2017 Bo Gan <ganb@vmware.com> 2.9.6-5
- Fix CVE-2016-6318, trigger for cracklib-dicts
- Trigger for dynamic symlink for dict
* Sun Nov 20 2016 Alexey Makhalov <amakhalov@vmware.com> 2.9.6-4
- Revert compressing pw_dict.pwd back. Python code
    cracklib.VeryFascistCheck does not handle it.
* Tue Nov 15 2016 Alexey Makhalov <amakhalov@vmware.com> 2.9.6-3
- Remove any dicts from cracklib main package
- Compress pw_dict.pwd file
- Move doc folder to devel package
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9.6-2
- GA - Bump release of all rpms
* Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> 2.9.6-1
- Updated to version 2.9.6
* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2.9.2-2
- Updated group.
