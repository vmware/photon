%define debug_package %{nil}
%global maj_ver vim80

Summary:        Text editor
Name:           vim
Version:        8.0.0533
Release:        13%{?dist}
License:        Charityware
URL:            http://www.vim.org
Group:          Applications/Editors
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        %{name}-%{version}.tar.gz
%define sha1    %{name}=6169cece15cb139db3ceff9c9ba2bf74013b1e02
Source1:        vimrc

BuildRequires:  ncurses-devel

Conflicts:      toybox < 0.7.3-7

Patch0:         CVE-2017-17087.patch
Patch1:         vim-CVE-2019-12735.patch
Patch2:         CVE-2019-20807.patch
Patch3:         vim-CVE-2021-3778.patch
Patch4:         vim-CVE-2021-3796.patch

%description
The VIM package contains a powerful text editor.

%package    extra
Summary:    Extra files for Vim text editor
Group:      Applications/Editors
Requires:   tcsh

%description extra
The vim extra package contains a extra files for powerful text editor.

%prep
%autosetup -p1
echo '#define SYS_VIMRC_FILE "/etc/vimrc"' >> src/feature.h

%build
%configure --enable-multibyte
make VERBOSE=1 %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
ln -sv vim %{buildroot}%{_bindir}/vi
install -vdm 755 %{buildroot}/etc
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/vimrc

%check
sed -i '/source test_recover.vim/d' src/testdir/test_alot.vim
make test %{?_smp_mflags}

%post
if ! sed -n -e '0,/[[:space:]]*call[[:space:]]\+system\>/p' %{_sysconfdir}/vimrc | \
     grep -q '^[[:space:]]*set[[:space:]]\+shell=/bin/bash'
then
    sed -i -e 's#^\([[:space:]]*\)\(call[[:space:]]\+system.*\)$#\1set shell=/bin/bash\n\1\2#g' \
        %{_sysconfdir}/vimrc
fi

%files extra
%defattr(-,root,root)
%{_bindir}/vimtutor
%{_bindir}/xxd
%{_mandir}/*/*
%doc %{_datarootdir}/vim/%{maj_ver}/doc/*
%{_datarootdir}/vim/%{maj_ver}/autoload/*
%{_datarootdir}/vim/%{maj_ver}/bugreport.vim
%{_datarootdir}/vim/%{maj_ver}/colors/*
%exclude %{_datarootdir}/vim/%{maj_ver}/colors/desert.vim
%{_datarootdir}/applications/gvim.desktop
%{_datarootdir}/applications/vim.desktop
%{_datarootdir}/icons/hicolor/48x48/apps/gvim.png
%{_datarootdir}/icons/locolor/16x16/apps/gvim.png
%{_datarootdir}/icons/locolor/32x32/apps/gvim.png
%{_datarootdir}/vim/%{maj_ver}/defaults.vim
%{_datarootdir}/vim/%{maj_ver}/pack/dist/opt/*
%{_datarootdir}/vim/%{maj_ver}/compiler/*
%{_datarootdir}/vim/%{maj_ver}/delmenu.vim
%{_datarootdir}/vim/%{maj_ver}/evim.vim
%{_datarootdir}/vim/%{maj_ver}/filetype.vim
%{_datarootdir}/vim/%{maj_ver}/ftoff.vim
%{_datarootdir}/vim/%{maj_ver}/ftplugin.vim
%{_datarootdir}/vim/%{maj_ver}/ftplugin/*
%{_datarootdir}/vim/%{maj_ver}/ftplugof.vim
%{_datarootdir}/vim/%{maj_ver}/gvimrc_example.vim
%{_datarootdir}/vim/%{maj_ver}/indent.vim
%{_datarootdir}/vim/%{maj_ver}/indent/*
%{_datarootdir}/vim/%{maj_ver}/indoff.vim
%{_datarootdir}/vim/%{maj_ver}/keymap/*
%{_datarootdir}/vim/%{maj_ver}/macros/*
%{_datarootdir}/vim/%{maj_ver}/menu.vim
%{_datarootdir}/vim/%{maj_ver}/mswin.vim
%{_datarootdir}/vim/%{maj_ver}/optwin.vim
%{_datarootdir}/vim/%{maj_ver}/plugin/*
%{_datarootdir}/vim/%{maj_ver}/synmenu.vim
%{_datarootdir}/vim/%{maj_ver}/vimrc_example.vim
%{_datarootdir}/vim/%{maj_ver}/print/*
%{_datarootdir}/vim/%{maj_ver}/scripts.vim
%{_datarootdir}/vim/%{maj_ver}/spell/*
%{_datarootdir}/vim/%{maj_ver}/syntax/*
%exclude %{_datarootdir}/vim/%{maj_ver}/syntax/syntax.vim
%{_datarootdir}/vim/%{maj_ver}/tools/*
%{_datarootdir}/vim/%{maj_ver}/tutor/*
%{_datarootdir}/vim/%{maj_ver}/lang/*.vim
%doc %{_datarootdir}/vim/%{maj_ver}/lang/*.txt
%lang(af) %{_datarootdir}/vim/%{maj_ver}/lang/af/LC_MESSAGES/vim.mo
%lang(ca) %{_datarootdir}/vim/%{maj_ver}/lang/ca/LC_MESSAGES/vim.mo
%lang(cs) %{_datarootdir}/vim/%{maj_ver}/lang/cs/LC_MESSAGES/vim.mo
%lang(de) %{_datarootdir}/vim/%{maj_ver}/lang/de/LC_MESSAGES/vim.mo
%lang(eb_GB) %{_datarootdir}/vim/%{maj_ver}/lang/en_GB/LC_MESSAGES/vim.mo
%lang(eo) %{_datarootdir}/vim/%{maj_ver}/lang/eo/LC_MESSAGES/vim.mo
%lang(es) %{_datarootdir}/vim/%{maj_ver}/lang/es/LC_MESSAGES/vim.mo
%lang(fi) %{_datarootdir}/vim/%{maj_ver}/lang/fi/LC_MESSAGES/vim.mo
%lang(fr) %{_datarootdir}/vim/%{maj_ver}/lang/fr/LC_MESSAGES/vim.mo
%lang(ga) %{_datarootdir}/vim/%{maj_ver}/lang/ga/LC_MESSAGES/vim.mo
%lang(it) %{_datarootdir}/vim/%{maj_ver}/lang/it/LC_MESSAGES/vim.mo
%lang(ja) %{_datarootdir}/vim/%{maj_ver}/lang/ja/LC_MESSAGES/vim.mo
%lang(ko.UTF-8) %{_datarootdir}/vim/%{maj_ver}/lang/ko.UTF-8/LC_MESSAGES/vim.mo
%lang(ko) %{_datarootdir}/vim/%{maj_ver}/lang/ko/LC_MESSAGES/vim.mo
%lang(nb) %{_datarootdir}/vim/%{maj_ver}/lang/nb/LC_MESSAGES/vim.mo
%lang(no) %{_datarootdir}/vim/%{maj_ver}/lang/no/LC_MESSAGES/vim.mo
%lang(pl) %{_datarootdir}/vim/%{maj_ver}/lang/pl/LC_MESSAGES/vim.mo
%lang(pt_BR) %{_datarootdir}/vim/%{maj_ver}/lang/pt_BR/LC_MESSAGES/vim.mo
%lang(ru) %{_datarootdir}/vim/%{maj_ver}/lang/ru/LC_MESSAGES/vim.mo
%lang(sk) %{_datarootdir}/vim/%{maj_ver}/lang/sk/LC_MESSAGES/vim.mo
%lang(sv) %{_datarootdir}/vim/%{maj_ver}/lang/sv/LC_MESSAGES/vim.mo
%lang(uk) %{_datarootdir}/vim/%{maj_ver}/lang/uk/LC_MESSAGES/vim.mo
%lang(vi) %{_datarootdir}/vim/%{maj_ver}/lang/vi/LC_MESSAGES/vim.mo
%lang(zh_CN.UTF-8) %{_datarootdir}/vim/%{maj_ver}/lang/zh_CN.UTF-8/LC_MESSAGES/vim.mo
%lang(zh_CN) %{_datarootdir}/vim/%{maj_ver}/lang/zh_CN/LC_MESSAGES/vim.mo
%lang(zh_TW.UTF-8) %{_datarootdir}/vim/%{maj_ver}/lang/zh_TW.UTF-8/LC_MESSAGES/vim.mo
%lang(zh_TW) %{_datarootdir}/vim/%{maj_ver}/lang/zh_TW/LC_MESSAGES/vim.mo
%lang(cs.cp1250)  %{_datarootdir}/vim/%{maj_ver}/lang/cs.cp1250/LC_MESSAGES/vim.mo
%lang(ja.euc-jp)  %{_datarootdir}/vim/%{maj_ver}/lang/ja.euc-jp/LC_MESSAGES/vim.mo
%lang(ja.sjis)    %{_datarootdir}/vim/%{maj_ver}/lang/ja.sjis/LC_MESSAGES/vim.mo
%lang(nl)     %{_datarootdir}/vim/%{maj_ver}/lang/nl/LC_MESSAGES/vim.mo
%lang(pl.UTF-8)   %{_datarootdir}/vim/%{maj_ver}/lang/pl.UTF-8/LC_MESSAGES/vim.mo
%lang(pl.cp1250)  %{_datarootdir}/vim/%{maj_ver}/lang/pl.cp1250/LC_MESSAGES/vim.mo
%lang(ru.cp1251)  %{_datarootdir}/vim/%{maj_ver}/lang/ru.cp1251/LC_MESSAGES/vim.mo
%lang(sk.cp1250)  %{_datarootdir}/vim/%{maj_ver}/lang/sk.cp1250/LC_MESSAGES/vim.mo
%lang(uk.cp1251)  %{_datarootdir}/vim/%{maj_ver}/lang/uk.cp1251/LC_MESSAGES/vim.mo
%lang(zh_CN.cp936) %{_datarootdir}/vim/%{maj_ver}/lang/zh_CN.cp936/LC_MESSAGES/vim.mo

%files
%defattr(-,root,root)
%config(noreplace) /etc/vimrc
%{_datarootdir}/vim/%{maj_ver}/colors/desert.vim
%{_datarootdir}/vim/%{maj_ver}/syntax/syntax.vim
%{_datarootdir}/vim/%{maj_ver}/rgb.txt
%{_bindir}/ex
%{_bindir}/vi
%{_bindir}/view
%{_bindir}/rvim
%{_bindir}/rview
%{_bindir}/vim
%{_bindir}/vimdiff

%changelog
* Thu Dec 02 2021 Shreenidhi Shedi <sshedi@vmware.com> 8.0.0533-13
- Enable skip_defaults_vim in vimrc
* Tue Nov 30 2021 Shreenidhi Shedi <sshedi@vmware.com> 8.0.0533-12
- Move vimrc to source file and add 'set mouse-=a' to /etc/vimrc
* Mon Oct 04 2021 Tapas Kundu <tkundu@vmware.com> 8.0.0533-11
- Fix for CVE-2021-3796
* Thu Sep 30 2021 Dweep Advani <dadvani@vmware.com> 8.0.0533-10
- Fix for CVE-2021-3778
* Mon Sep 13 2021 Shreenidhi Shedi <sshedi@vmware.com> 8.0.0533-9
- Conflict only with toybox < 0.7.3-7
* Wed Jun 03 2020 Anisha Kumari <kanisha@vmwre.com> 8.0.0533-8
- Fix for CVE-2019-20807
* Thu Jun 06 2019 Siju Maliakkal <smaliakkal@vmwre.com> 8.0.0533-7
- Fix for CVE-2019-12735
* Tue Jan 29 2019 Dweep Advani <dadvani@vmware.com> 8.0.0533-6
- Fixed swap file creation error for custom login shell
* Thu Jul 12 2018 Tapas Kundu <tkundu@vmware.com> 8.0.0533-5
- Fix for CVE-2017-1000382
* Tue Jul 10 2018 Tapas Kundu <tkundu@vmware.com> 8.0.0533-4
- Fix for CVE-2017-17087.patch.
* Mon Aug 14 2017 Chang Lee <changlee@vmware.com>  8.0.0533-3
- Disabled Test_recover_root_dir in %check
* Tue May 02 2017 Anish Swaminathan <anishs@vmware.com>  8.0.0533-2
- Remove tcsh requires
* Fri Apr 14 2017 Xiaolin Li <xiaolinl@vmware.com> 8.0.0533-1
- Updated to version 8.0.0533.
* Tue Feb 28 2017 Anish Swaminathan <anishs@vmware.com>  7.4-10
- Fix for CVE-2017-6349 and CVE-2017-6350
* Fri Feb 17 2017 Anish Swaminathan <anishs@vmware.com>  7.4-9
- Fix for CVE-2017-5953
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  7.4-8
- Fix for CVE-2016-1248
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 7.4-7
- Modified %check
* Wed Aug 24 2016 Alexey Makhalov <amakhalov@vmware.com> 7.4-6
- vimrc: Added tags search, tab->spaces and some bindings
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.4-5
- GA - Bump release of all rpms
* Thu Jul 16 2015 Touseef Liaqat <tliaqat@vmware.com> 7.4-3
- Added profile related files in minimal vim package.
* Tue Jun 30 2015 Touseef Liaqat <tliaqat@vmware.com> 7.4-3
- Pack extra files separately, to make vim package small.
* Fri Jun 19 2015 Alexey Makhalov <amakhalov@vmware.com> 7.4-2
- Disable debug package. Use 'desert' colorscheme.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 7.4-1
- Initial build. First version
