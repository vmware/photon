%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           tuna
Version:        0.17
Release:        1%{?dist}
License:        GPLv2
Summary:        Application tuning command line utility
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rt.wiki.kernel.org/index.php/Tuna
Source:         https://www.kernel.org/pub/software/utils/%{name}/%{name}-%{version}.tar.xz
%define sha512  tuna=e04bb56415e702e888d7022342e34bdff19fe978e13793e737613baf48eadcd1b926d414ec8ba5205c9bea4622bf44b9b12e1fe33e1a89b467bd84e17c4643c4
BuildArch:      noarch
BuildRequires:  python3-devel, gettext
Requires:       python3-ethtool
Requires:       python3-linux-procfs
Requires:       python3-schedutils

%description
Provides command line interface for changing scheduler and IRQ tunables,
at whole CPU and at per thread/IRQ level. Allows isolating CPUs for use by
a specific application and moving threads and interrupts to a CPU.
Operations can be done on CPU sockets, understanding CPU topology.

%prep
%autosetup

%build
python3 setup.py build

%install
rm -rf %{buildroot}
python3 setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}/%{_sysconfdir}/tuna/
mkdir -p %{buildroot}/{%{_bindir},%{_datadir}/tuna/help/kthreads,%{_mandir}/man8}
mkdir -p %{buildroot}/%{_datadir}/polkit-1/actions/
install -p -m755 tuna-cmd.py %{buildroot}/%{_bindir}/tuna
install -p -m644 help/kthreads/* %{buildroot}/%{_datadir}/tuna/help/kthreads/
install -p -m644 docs/tuna.8 %{buildroot}/%{_mandir}/man8/
install -p -m644 etc/tuna/example.conf %{buildroot}/%{_sysconfdir}/tuna/
install -p -m644 etc/tuna.conf %{buildroot}/%{_sysconfdir}/
install -p -m644 org.tuna.policy %{buildroot}/%{_datadir}/polkit-1/actions/

# l10n-ed message catalogues
for lng in `cat po/LINGUAS`; do
        po=po/"$lng.po"
        mkdir -p %{buildroot}/%{_datadir}/locale/${lng}/LC_MESSAGES
        msgfmt $po -o %{buildroot}/%{_datadir}/locale/${lng}/LC_MESSAGES/%{name}.mo
done

%find_lang %name

%files -f %{name}.lang
%defattr(0755,root,root,0755)
%doc ChangeLog
%{python3_sitelib}/*.egg-info
%{_bindir}/tuna
%{_datadir}/tuna/
%{python3_sitelib}/tuna/
%{_mandir}/man8/tuna.8*
%config(noreplace) %{_sysconfdir}/tuna.conf
%config(noreplace) %{_sysconfdir}/tuna/*
%{_datadir}/polkit-1/actions/org.tuna.policy

%changelog
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 0.17-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.14.1-1
- Automatic Version Bump
* Tue Jun 16 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 0.14-2
- Remove unnecessary version constraint for runtime package dependency.
* Thu Mar 19 2020 Shreyas B. <shreyasb@vmware.com> 0.14-1
- Initial version of tuna spec.
