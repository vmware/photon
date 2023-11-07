%define debug_package %{nil}
%global maj_ver vim82

Summary:        Text editor
Name:           vim
Version:        8.2.5169
Release:        13%{?dist}
License:        Charityware
URL:            http://www.vim.org
Group:          Applications/Editors
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        %{name}-%{version}.tar.gz
%define sha512  %{name}=e2b85746a4cc9ce2a4deeb0a3cd0365ad3124492b2c0feb4e029c7f58a960382bc0d3f3f4611742fa7a8559204f711c831407289b113386fce1138e3c9fc3c75
Source1:        vimrc

Patch0:  CVE-2022-47024.patch
Patch1:  CVE-2023-0433.patch
Patch2:  CVE-2023-0049.patch
Patch3:  CVE-2023-0051.patch
Patch4:  CVE-2023-0054.patch
Patch5:  CVE-2022-3520.patch
Patch6:  CVE-2022-4292.patch
Patch7:  CVE-2022-2946.patch
Patch8:  CVE-2022-3591.patch
Patch9:  CVE-2022-2819.patch
Patch10: backport-for-CVE-2022-3324.patch
Patch11: CVE-2022-3324.patch
Patch12: CVE-2023-1264.patch
Patch13: CVE-2023-1175.patch
Patch14: CVE-2023-1170.patch
Patch15: CVE-2022-3352.patch
Patch16: CVE-2022-3256.patch
Patch17: CVE-2022-3235.patch
Patch18: CVE-2022-4141.patch
Patch19: CVE-2022-3099.patch
Patch20: CVE-2022-2874.patch
Patch21: CVE-2022-2343.patch
Patch22: CVE-2022-3134.patch
Patch23: CVE-2022-2849.patch
Patch24: CVE-2022-2285.patch
Patch25: CVE-2022-3234.patch
Patch26: CVE-2022-3297.patch
Patch27: CVE-2022-2286.patch
Patch28: CVE-2022-2345.patch
Patch29: CVE-2022-2581.patch
Patch30: CVE-2022-2522.patch
Patch31: CVE-2022-2889.patch
Patch32: CVE-2022-3296.patch
Patch33: CVE-2022-2598.patch
Patch34: CVE-2022-2982.patch
Patch35: CVE-2022-2845.patch
Patch36: CVE-2022-2571.patch
Patch37: CVE-2022-3016.patch
Patch38: CVE-2022-2289.patch
Patch39: CVE-2022-2344.patch
Patch40: CVE-2022-3037.patch
Patch41: CVE-2022-2287.patch
Patch42: CVE-2022-2257.patch
Patch43: CVE-2022-2284.patch
Patch44: CVE-2022-2264.patch
Patch45: CVE-2022-2980.patch
Patch46: CVE-2022-2817.patch
Patch47: CVE-2022-2580.patch
Patch48: CVE-2022-2288.patch
Patch49: CVE-2022-2816.patch
Patch50: CVE-2022-2862.patch
Patch51: CVE-2022-2923.patch
Patch52: CVE-2022-2304.patch
Patch53: CVE-2022-3491.patch
Patch54: backport-for-CVE-2022-4293.patch
Patch55: CVE-2022-4293.patch
Patch56: CVE-2022-3705.patch
Patch57: CVE-2022-3153.patch
Patch58: CVE-2022-3278.patch
Patch59: CVE-2023-2426.patch
Patch60: CVE-2023-2610.patch
Patch61: CVE-2023-2609.patch
Patch62: CVE-2023-4734.patch
Patch63: CVE-2023-4735.patch
Patch64: CVE-2023-4736.patch
Patch65: CVE-2023-4751.patch
Patch66: CVE-2023-4733.patch
Patch67: CVE-2023-4738.patch
Patch68: backport-for-CVE-2023-4750.patch
Patch69: CVE-2023-4750.patch
Patch70: CVE-2023-4752.patch
Patch71: CVE-2023-4781.patch
Patch72: CVE-2023-5344.patch
Patch73: CVE-2023-5441.patch
Patch74: CVE-2023-5535.patch
Patch75: CVE-2023-46246.patch

BuildRequires:  ncurses-devel >= 6.1-4
Requires:       ncurses-libs >= 6.1-4

%description
The VIM package contains a powerful text editor.

%package    extra
Summary:    Extra files for Vim text editor
Group:      Applications/Editors
Requires:   tcsh
Requires:   %{name} = %{version}-%{release}
Conflicts:  toybox < 0.8.2-2

%description extra
The vim extra package contains a extra files for powerful text editor.

%prep
%autosetup -p1
echo '#define SYS_VIMRC_FILE "/etc/vimrc"' >> src/feature.h

%build
%configure \
    --enable-multibyte

%make_build

%install
# make doesn't support _smp_mflags
%make_install
ln -sfv vim %{buildroot}%{_bindir}/vi
install -vdm 755 %{buildroot}%{_sysconfdir}
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/vimrc

%if 0%{?with_check}
%check
sed -i '/source test_recover.vim/d' src/testdir/test_alot.vim
sed -i '916d' src/testdir/test_search.vim
sed -i '454,594d' src/testdir/test_autocmd.vim
sed -i '1,9d' src/testdir/test_modeline.vim
sed -i '133d' ./src/testdir/Make_all.mak
make test %{?_smp_mflags}
%endif

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
%{_datarootdir}/applications/gvim.desktop
%{_datarootdir}/applications/vim.desktop
%{_datarootdir}/icons/hicolor/48x48/apps/gvim.png
%{_datarootdir}/icons/locolor/16x16/apps/gvim.png
%{_datarootdir}/icons/locolor/32x32/apps/gvim.png
%{_datarootdir}/vim/%{maj_ver}/pack/dist/opt/*
%exclude %{_datarootdir}/vim/%{maj_ver}/colors/desert.vim
%exclude %{_datarootdir}/vim/%{maj_ver}/colors/lists/default.vim
%{_datarootdir}/vim/%{maj_ver}/compiler/*
%{_datarootdir}/vim/%{maj_ver}/delmenu.vim
%{_datarootdir}/vim/%{maj_ver}/evim.vim
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
%{_datarootdir}/vim/%{maj_ver}/import/dist/vimhelp.vim
%{_datarootdir}/vim/%{maj_ver}/spell/*
%{_datarootdir}/vim/%{maj_ver}/syntax/*
%exclude %{_datarootdir}/vim/%{maj_ver}/syntax/nosyntax.vim
%exclude %{_datarootdir}/vim/%{maj_ver}/syntax/syntax.vim
%exclude %{_datarootdir}/vim/%{maj_ver}/autoload/dist/ft.vim
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
%lang(da) %{_datarootdir}/vim/%{maj_ver}/lang/da/LC_MESSAGES/vim.mo
%lang(lv) %{_datarootdir}/vim/%{maj_ver}/lang/lv/LC_MESSAGES/vim.mo
%lang(sr) %{_datarootdir}/vim/%{maj_ver}/lang/sr/LC_MESSAGES/vim.mo
%lang(vi) %{_datarootdir}/vim/%{maj_ver}/lang/vi/LC_MESSAGES/vim.mo
%lang(tr) %{_datarootdir}/vim/%{maj_ver}/lang/tr/LC_MESSAGES/vim.mo
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
%config(noreplace) %{_sysconfdir}/vimrc
%{_datarootdir}/vim/%{maj_ver}/defaults.vim
%{_datarootdir}/vim/%{maj_ver}/filetype.vim
%{_datarootdir}/vim/%{maj_ver}/colors/desert.vim
%{_datarootdir}/vim/%{maj_ver}/colors/lists/default.vim
%{_datarootdir}/vim/%{maj_ver}/syntax/nosyntax.vim
%{_datarootdir}/vim/%{maj_ver}/syntax/syntax.vim
%{_datarootdir}/vim/%{maj_ver}/autoload/dist/ft.vim
%{_bindir}/ex
%{_bindir}/vi
%{_bindir}/view
%{_bindir}/rvim
%{_bindir}/rview
%{_bindir}/vim
%{_bindir}/vimdiff

%changelog
* Mon Nov 06 2023 Srish Srinivasan <ssrish@vmware.com> 8.2.5169-13
- patched CVE-2023-46246
* Tue Oct 10 2023 Srish Srinivasan <ssrish@vmware.com> 8.2.5169-12
- patched CVE-2023-5344, CVE-2023-5441, and CVE-2023-5535
* Mon Sep 11 2023 Srish Srinivasan <ssrish@vmware.com> 8.2.5169-11
- Fix multiple CVEs
* Wed Sep 06 2023 Mukul Sikka <msikka@vmware.com> 8.2.5169-10
- Fix multiple CVEs
* Thu May 25 2023 Srish Srinivasan <ssrish@vmware.com> 8.2.5169-9
- Fix CVE-2023-2609
* Thu May 18 2023 Srish Srinivasan <ssrish@vmware.com> 8.2.5169-8
- Fix CVE-2023-2610
* Tue May 09 2023 Srish Srinivasan <ssrish@vmware.com> 8.2.5169-7
- fix CVE-2023-2426
* Mon Mar 27 2023 Srish Srinivasan <ssrish@vmware.com> 8.2.5169-6
- fixed multiple P2 CVEs
- CVE-2023-1264, CVE-2023-1175, CVE-2023-1170, CVE-2022-3352
- CVE-2022-3256, CVE-2022-3235, CVE-2022-4141, CVE-2022-3099
- CVE-2022-2874, CVE-2022-2343, CVE-2022-3134, CVE-2022-2849
- CVE-2022-2285, CVE-2022-3234, CVE-2022-3297, CVE-2022-2286
- CVE-2022-2345, CVE-2022-2581, CVE-2022-2522, CVE-2022-2889
- CVE-2022-3296, CVE-2022-2598, CVE-2022-2982, CVE-2022-2845
- CVE-2022-2571, CVE-2022-3016, CVE-2022-2289, CVE-2022-2344
- CVE-2022-3037, CVE-2022-2287, CVE-2022-2257, CVE-2022-2284
- CVE-2022-2264, CVE-2022-2980, CVE-2022-2817, CVE-2022-2580
- CVE-2022-2288, CVE-2022-2816, CVE-2022-2862, CVE-2022-2923
- CVE-2022-2304, CVE-2022-3491, CVE-2022-4293, CVE-2022-3705
- CVE-2022-3153, CVE-2022-3278
* Tue Feb 7 2023 Srish Srinivasan <ssrish@vmware.com> 8.2.5169-5
- fixed multiple P1 CVEs
- CVE-2022-3520, CVE-2022-4292, CVE-2022-2946
- CVE-2022-3591, CVE-2022-2819, CVE-2022-3324
* Tue Feb 7 2023 Srish Srinivasan <ssrish@vmware.com> 8.2.5169-4
- fix CVE-2023-0433.patch, CVE-2023-0049.patch, CVE-2023-0051.patch, and CVE-2023-0054.patch
* Mon Jan 30 2023 Srish Srinivasan <ssrish@vmware.com> 8.2.5169-3
- fix for CVE-2022-47024
* Mon Jan 16 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.2.5169-2
- Handle E145 exception in vimrc when vim opened in restricted mode
* Tue Jul 26 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.5169-1
- Update to 8.2.5169 to fix CVE-2022-2231
* Sat Jul 09 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.5164-1
- Update to 8.2.5164 to fix CVE-2022-2207, CVE-2022-2210
* Fri Jul 01 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.5151-1
- Update to 8.2.5151 to fix several CVEs
* Wed Jun 22 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.5043-1
- Update to 8.2.5043 to fix CVE-2022-1942
* Tue Jun 14 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.5037-1
- Update to 8.2.5037 to fix CVE-2022-1927
* Fri Jun 10 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.5024-1
- Update to 8.2.5024 to fix several CVEs
* Wed May 18 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.4925-1
- Update to 8.2.4925 to fix several CVEs
* Tue Apr 26 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.4827-1
- Update to 8.2.4827 to fix CVE-2022-1381
* Thu Apr 07 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.4647-1
- Update to 8.2.4647 to fix CVE-2022-1160
* Tue Apr 05 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.4646-1
- Update to 8.2.4646 to fix several CVEs
* Thu Mar 17 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.3408-25
- Fix CVE-2022-0417
* Wed Mar 16 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.3408-24
- Fix CVE-2022-0714,CVE-2022-0319,CVE-2021-4193
* Fri Mar 11 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.3408-23
- Fix CVE-2022-0572
* Mon Mar 07 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.3408-22
- Fix CVE-2022-0729,CVE-2022-0554
* Tue Mar 01 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.3408-21
- Fix CVE-2022-0629,CVE-2022-0685
* Thu Feb 17 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.3408-20
- Fix CVE-2022-0368
* Wed Feb 16 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.3408-19
- Fix CVE-2022-0443,CVE-2022-0413,CVE-2022-0392,CVE-2022-0407
* Fri Feb 11 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.3408-18
- Fix CVE-2022-0359,CVE-2022-0361,CVE-2022-0408
* Tue Feb 08 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.3408-17
- Fix CVE-2021-4173
* Thu Feb 03 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.3408-16
- Fix CVE-2022-0128
* Wed Feb 02 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.3408-15
- Fix CVE-2021-4166,CVE-2021-4187,CVE-2021-4192
* Tue Feb 01 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.3408-14
- Fix CVE-2022-0261, format patch CVE-2022-0318
* Mon Jan 31 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.3408-13
- Fix CVE-2022-0318
* Mon Jan 24 2022 Harinadh D <hdommaraju@vmware.com> 8.2.3408-12
- Fix CVE-2021-4136
* Tue Jan 11 2022 Piyush Gupta <gpiyush@vmware.com> 8.2.3408-11
- Added Requires ncurses-libs.
* Wed Dec 15 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.3408-10
- Fix CVE-2021-4069
* Tue Dec 14 2021 Harinadh D <hdommaraju@vmware.com> 8.2.3408-9
- Fix CVE-2021-4019,CVE-2021-3984
* Wed Dec 08 2021 Mukul Sikka <msikka@vmware.com> 8.2.3408-8
- Fix for CVE-2021-3903, CVE-2021-3927 and CVE-2021-3928
* Tue Dec 07 2021 Shreenidhi Shedi <sshedi@vmware.com> 8.2.3408-7
- Enable skip_defaults_vim in vimrc
* Tue Nov 30 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.3408-6
- Fix CVE-2021-3973, CVE-2021-3974
* Mon Oct 25 2021 Dweep Advani <tkundu@vmware.com> 8.2.3408-5
- Fix for CVE-2021-3872 and CVE-2021-3875
* Mon Oct 04 2021 Tapas Kundu <tkundu@vmware.com> 8.2.3408-4
- Fix for CVE-2021-3796
* Thu Sep 30 2021 Dweep Advani <dadvani@vmware.com> 8.2.3408-3
- Fix for CVE-2021-3778
* Thu Sep 23 2021 Dweep Advani <davani@vmware.com> 8.2.3408-2
- Fix vim startup errors E216, E1187 and E484
- vim-extra requires vim
* Wed Sep 15 2021 Tapas Kundu <tkundu@vmware.com> 8.2.3408-1
- Fix CVE-2021-3770
* Fri Jul 03 2020 Prashant S Chauhan <psinghchauha@vmware.com> 8.1.1365-2
- Do not conflict with toybox >= 0.8.2-2
* Thu Jun 04 2020 Tapas Kundu <tkundu@vmware.com> 8.1.1365-1
- Update to 8.1.1365 to take Ex command changes along with CVE-2019-20807
* Mon Jun 1 2020 Anisha Kumari <kanisha@vmware.com> 8.1.0388-7
- Fix for CVE-2019-20807.
* Thu Feb 20 2020 Prashant Singh Chauhan <psinghchauha@vmware.com> 8.1.0388-6
- Fix make check failure
* Wed Sep 25 2019 Prashant Singh Chauhan <psinghchauha@vmware.com> 8.1.0388-5
- Removed tests since make-check job was getting stuck on that test
* Wed Aug 14 2019 Anisha Kumari <kanisha@vmware.com> 8.1.0388-4
- Fix for CVE-2019-12735.
* Tue Jan 29 2019 Dweep Advani <dadvani@vmware.com> 8.1.0388-3
- Fixed swap file creation error for custom login shell
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 8.1.0388-2
- Add conflicts toybox for vim-extra.
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 8.1.0388-1
- Update to version 8.1.0388.
* Tue Jul 10 2018 Tapas Kundu <tkundu@vmware.com> 8.0.0533-4
- Fix for CVE-2017-17087 and CVE-2017-1000382.
* Mon Aug 14 2017 Chang Lee <changlee@vmware.com>  8.0.0533-3
- Disabled Test_recover_root_dir in %check.
* Tue May 02 2017 Anish Swaminathan <anishs@vmware.com>  8.0.0533-2
- Remove tcsh requires.
* Fri Apr 14 2017 Xiaolin Li <xiaolinl@vmware.com> 8.0.0533-1
- Updated to version 8.0.0533.
* Tue Feb 28 2017 Anish Swaminathan <anishs@vmware.com>  7.4-10
- Fix for CVE-2017-6349 and CVE-2017-6350.
* Fri Feb 17 2017 Anish Swaminathan <anishs@vmware.com>  7.4-9
- Fix for CVE-2017-5953.
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  7.4-8
- Fix for CVE-2016-1248.
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 7.4-7
- Modified %check.
* Wed Aug 24 2016 Alexey Makhalov <amakhalov@vmware.com> 7.4-6
- vimrc: Added tags search, tab->spaces and some bindings.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.4-5
- GA - Bump release of all rpms.
* Thu Jul 16 2015 Touseef Liaqat <tliaqat@vmware.com> 7.4-3
- Added profile related files in minimal vim package.
* Tue Jun 30 2015 Touseef Liaqat <tliaqat@vmware.com> 7.4-3
- Pack extra files separately, to make vim package small.
* Fri Jun 19 2015 Alexey Makhalov <amakhalov@vmware.com> 7.4-2
- Disable debug package. Use 'desert' colorscheme.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 7.4-1
- Initial build First version.
