%define debug_package %{nil}

Summary:    Text editor
Name:       vim
Version:    7.4
Release:    11%{?dist}
License:    Charityware
URL:        http://www.vim.org
Group:      Applications/Editors
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    %{name}-%{version}.tar.bz2
%define sha1 vim=601abf7cc2b5ab186f40d8790e542f86afca86b7
Patch0:         vim-CVE-2016-1248.patch
Patch1:         vim-7.4-CVE-2017-5953.patch
Patch2:         vim-7.4-CVE-2017-6349_CVE-2017-6350.patch
BuildRequires:  ncurses-devel >= 6.0-3
Requires:  ncurses >= 6.0-3
Requires:   tcsh

%description
The Vim package contains a powerful text editor.

%package    extra
Summary:    Extra files for Vim text editor
Group:      Applications/Editors
Requires:   tcsh

%description extra
The vim extra package contains a extra files for powerful text editor.

%prep
%setup -q -n %{name}74
%patch0 -p1
%patch1 -p1
%patch2 -p1
echo '#define SYS_VIMRC_FILE "/etc/vimrc"' >> src/feature.h

%build
./configure \
    --prefix=%{_prefix} \
    --enable-multibyte
make VERBOSE=1 %{?_smp_mflags}

%install
cd %{_builddir}/%{name}74
make DESTDIR=%{buildroot} install
ln -sv vim %{buildroot}%{_bindir}/vi
install -vdm 755 %{buildroot}/etc
cat > %{buildroot}/etc/vimrc << "EOF"
" Begin /etc/vimrc

set shell=/bin/bash
set nocompatible
set backspace=2
set ruler
syntax on
color desert
if (&term == "iterm") || (&term == "putty")
  set background=dark
endif
" Move the swap file location to protect against CVE-2017-1000382
" More information at http://security.cucumberlinux.com/security/details.php?id=120
if ! isdirectory("~/.vim/swap/")
        call system('install -d -m 700 ~/.vim/swap')
endif
set directory=~/.vim/swap//
" End /etc/vimrc
EOF

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
%doc %{_datarootdir}/vim/vim74/doc/*
%{_datarootdir}/vim/vim74/autoload/*
%{_datarootdir}/vim/vim74/bugreport.vim
%{_datarootdir}/vim/vim74/colors/*
%exclude %{_datarootdir}/vim/vim74/colors/desert.vim
%{_datarootdir}/vim/vim74/compiler/*
%{_datarootdir}/vim/vim74/delmenu.vim
%{_datarootdir}/vim/vim74/evim.vim
%{_datarootdir}/vim/vim74/filetype.vim
%{_datarootdir}/vim/vim74/ftoff.vim
%{_datarootdir}/vim/vim74/ftplugin.vim
%{_datarootdir}/vim/vim74/ftplugin/*
%{_datarootdir}/vim/vim74/ftplugof.vim
%{_datarootdir}/vim/vim74/gvimrc_example.vim
%{_datarootdir}/vim/vim74/indent.vim
%{_datarootdir}/vim/vim74/indent/*
%{_datarootdir}/vim/vim74/indoff.vim
%{_datarootdir}/vim/vim74/keymap/*
%{_datarootdir}/vim/vim74/macros/*
%{_datarootdir}/vim/vim74/menu.vim
%{_datarootdir}/vim/vim74/mswin.vim
%{_datarootdir}/vim/vim74/optwin.vim
%{_datarootdir}/vim/vim74/plugin/*
%{_datarootdir}/vim/vim74/synmenu.vim
%{_datarootdir}/vim/vim74/vimrc_example.vim
%{_datarootdir}/vim/vim74/print/*
%{_datarootdir}/vim/vim74/scripts.vim
%{_datarootdir}/vim/vim74/spell/*
%{_datarootdir}/vim/vim74/syntax/*
%exclude %{_datarootdir}/vim/vim74/syntax/syntax.vim
%{_datarootdir}/vim/vim74/tools/*
%{_datarootdir}/vim/vim74/tutor/*
%{_datarootdir}/vim/vim74/lang/*.vim
%doc %{_datarootdir}/vim/vim74/lang/*.txt
%lang(af) %{_datarootdir}/vim/vim74/lang/af/LC_MESSAGES/vim.mo
%lang(ca) %{_datarootdir}/vim/vim74/lang/ca/LC_MESSAGES/vim.mo
%lang(cs) %{_datarootdir}/vim/vim74/lang/cs/LC_MESSAGES/vim.mo
%lang(de) %{_datarootdir}/vim/vim74/lang/de/LC_MESSAGES/vim.mo
%lang(eb_GB) %{_datarootdir}/vim/vim74/lang/en_GB/LC_MESSAGES/vim.mo
%lang(eo) %{_datarootdir}/vim/vim74/lang/eo/LC_MESSAGES/vim.mo
%lang(es) %{_datarootdir}/vim/vim74/lang/es/LC_MESSAGES/vim.mo
%lang(fi) %{_datarootdir}/vim/vim74/lang/fi/LC_MESSAGES/vim.mo
%lang(fr) %{_datarootdir}/vim/vim74/lang/fr/LC_MESSAGES/vim.mo
%lang(ga) %{_datarootdir}/vim/vim74/lang/ga/LC_MESSAGES/vim.mo
%lang(it) %{_datarootdir}/vim/vim74/lang/it/LC_MESSAGES/vim.mo
%lang(ja) %{_datarootdir}/vim/vim74/lang/ja/LC_MESSAGES/vim.mo
%lang(ko.UTF-8) %{_datarootdir}/vim/vim74/lang/ko.UTF-8/LC_MESSAGES/vim.mo
%lang(ko) %{_datarootdir}/vim/vim74/lang/ko/LC_MESSAGES/vim.mo
%lang(nb) %{_datarootdir}/vim/vim74/lang/nb/LC_MESSAGES/vim.mo
%lang(no) %{_datarootdir}/vim/vim74/lang/no/LC_MESSAGES/vim.mo
%lang(pl) %{_datarootdir}/vim/vim74/lang/pl/LC_MESSAGES/vim.mo
%lang(pt_BR) %{_datarootdir}/vim/vim74/lang/pt_BR/LC_MESSAGES/vim.mo
%lang(ru) %{_datarootdir}/vim/vim74/lang/ru/LC_MESSAGES/vim.mo
%lang(sk) %{_datarootdir}/vim/vim74/lang/sk/LC_MESSAGES/vim.mo
%lang(sv) %{_datarootdir}/vim/vim74/lang/sv/LC_MESSAGES/vim.mo
%lang(uk) %{_datarootdir}/vim/vim74/lang/uk/LC_MESSAGES/vim.mo
%lang(vi) %{_datarootdir}/vim/vim74/lang/vi/LC_MESSAGES/vim.mo
%lang(zh_CN.UTF-8) %{_datarootdir}/vim/vim74/lang/zh_CN.UTF-8/LC_MESSAGES/vim.mo
%lang(zh_CN) %{_datarootdir}/vim/vim74/lang/zh_CN/LC_MESSAGES/vim.mo
%lang(zh_TW.UTF-8) %{_datarootdir}/vim/vim74/lang/zh_TW.UTF-8/LC_MESSAGES/vim.mo
%lang(zh_TW) %{_datarootdir}/vim/vim74/lang/zh_TW/LC_MESSAGES/vim.mo
%lang(cs.cp1250)  %{_datarootdir}/vim/vim74/lang/cs.cp1250/LC_MESSAGES/vim.mo
%lang(ja.euc-jp)  %{_datarootdir}/vim/vim74/lang/ja.euc-jp/LC_MESSAGES/vim.mo
%lang(ja.sjis)    %{_datarootdir}/vim/vim74/lang/ja.sjis/LC_MESSAGES/vim.mo
%lang(nl)     %{_datarootdir}/vim/vim74/lang/nl/LC_MESSAGES/vim.mo
%lang(pl.UTF-8)   %{_datarootdir}/vim/vim74/lang/pl.UTF-8/LC_MESSAGES/vim.mo
%lang(pl.cp1250)  %{_datarootdir}/vim/vim74/lang/pl.cp1250/LC_MESSAGES/vim.mo
%lang(ru.cp1251)  %{_datarootdir}/vim/vim74/lang/ru.cp1251/LC_MESSAGES/vim.mo
%lang(sk.cp1250)  %{_datarootdir}/vim/vim74/lang/sk.cp1250/LC_MESSAGES/vim.mo
%lang(uk.cp1251)  %{_datarootdir}/vim/vim74/lang/uk.cp1251/LC_MESSAGES/vim.mo
%lang(zh_CN.cp936) %{_datarootdir}/vim/vim74/lang/zh_CN.cp936/LC_MESSAGES/vim.mo

%files
%defattr(-,root,root)
%config(noreplace) /etc/vimrc
%{_datarootdir}/vim/vim74/colors/desert.vim
%{_datarootdir}/vim/vim74/syntax/syntax.vim
%{_bindir}/ex
%{_bindir}/vi
%{_bindir}/view
%{_bindir}/rvim
%{_bindir}/rview
%{_bindir}/vim
%{_bindir}/vimdiff

%changelog
*   Tue Jan 29 2019 Dweep Advani <dadvani@vmware.com> 7.4-11
-   Fixed swap file creation error for custom login shell
*   Thu Jul 12 2018 Tapas Kundu <tkundu@vmware.com> 7.4-10
-   Fix for CVE-2017-1000382
*   Mon Apr 3 2017 Alexey Makhalov <amakhalov@vmware.com> 7.4-9
-   Use specified version of ncurses wich has long chtype and mmask_t
    (see ncurses changelog)
*   Tue Feb 28 2017 Anish Swaminathan <anishs@vmware.com>  7.4-8
-   Fix for CVE-2017-6349 and CVE-2017-6350
*   Fri Feb 17 2017 Anish Swaminathan <anishs@vmware.com>  7.4-7
-   Fix for CVE-2017-5953
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  7.4-6
-   Fix for CVE-2016-1248
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.4-5
-   GA - Bump release of all rpms
*   Thu Jul 16 2015 Touseef Liaqat <tliaqat@vmware.com> 7.4-3
-   Added profile related files in minimal vim package.
*   Tue Jun 30 2015 Touseef Liaqat <tliaqat@vmware.com> 7.4-3
-   Pack extra files separately, to make vim package small.
*   Fri Jun 19 2015 Alexey Makhalov <amakhalov@vmware.com> 7.4-2
-   Disable debug package. Use 'desert' colorscheme.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 7.4-1
-   Initial build.  First version
