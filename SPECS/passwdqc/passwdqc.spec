Summary:        Simple Password Strength Checking Module
Name:           passwdqc
Version:        2.0.2
License:        BSD-compatible
Release:        2%{?dist}
Url:            http://www.openwall.com/passwdqc
Group:          System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://www.openwall.com/passwdqc/%{name}-%{version}.tar.gz
%define sha512  %{name}=60f91ad7c86314b0d9ad97a2474a1a5bbb8b41491b274e09f7300d8a609cfffb0688bf39d4e715f647f3c87bfee429cb5e01f1a641a14eea3f55b223610ed8ec

BuildRequires:  Linux-PAM-devel

%description
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policies without
having to recompile programs that do authentication.

pam_passwdqc is a simple password strength checking module forPAM-aware
password changing programs. In addition to checking regular passwords,
it offers support for passphrases and can provide randomly generated
ones.

%package -n passwdqc-devel
Summary:  Useful collection of routines for C and C++ programming
Group:    Development/Libraries/C and C++
Requires: %{name} = %{version}-%{release}

%description -n passwdqc-devel
This package contains development libraries and header files needed for
building passwdqc-aware applications.

%prep
%autosetup -p1

%build
EXTRA_CFLAGS="-fno-strict-aliasing"
make CFLAGS="%{optflags} ${EXTRA_CFLAGS} -fPIC -DHAVE_SHADOW -DLINUX_PAM" \
     SHARED_LIBDIR="%{_lib}" \
     DEVEL_LIBDIR="%{_libdir}" \
     SECUREDIR="%{_lib}/security" %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} SHARED_LIBDIR="%{_lib}" \
    DEVEL_LIBDIR="%{_libdir}" SECUREDIR="%{_lib}/security" install %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%if 0%{?with_check}
%check
# Check for module problems.  Specifically, check that every module we just
# installed can actually be loaded by a minimal PAM-aware application.
export LD_LIBRARY_PATH="%{buildroot}%{_lib}"
for module in %{buildroot}%{_lib}/security/pam*.so ; do
  if ! sh %{_sourcedir}/dlopen.sh -lpam -ldl ${module} ; then
    exit 1
  fi
done
%endif

%files
%defattr(-,root,root)
%doc LICENSE README pwqcheck.php
%config(noreplace) %{_sysconfdir}/passwdqc.conf
%{_lib}/lib*.so*
%{_bindir}/*
%{_lib}/security/pam_passwdqc.so
%{_mandir}/man*/*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/lib*.so

%changelog
* Wed Feb 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.0.2-2
- Fix binary path
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.0.2-1
- Automatic Version Bump
* Thu Apr 02 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 1.4.0-1
- Add package passwdqc at version 1.4.0
