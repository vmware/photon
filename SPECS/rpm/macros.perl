# Perl specific macro definitions.

%__perl         %{_bindir}/perl
%perl_sitelib	%(eval "`perl -V:installsitelib`"; echo $installsitelib)
%perl_sitearch	%(eval "`perl -V:installsitearch`"; echo $installsitearch)
%perl_archlib	%(eval "`perl -V:installarchlib`"; echo $installarchlib)
%perl_privlib	%(eval "`perl -V:installprivlib`"; echo $installprivlib)
