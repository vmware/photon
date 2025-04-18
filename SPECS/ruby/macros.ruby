%gem_binary                        %{_bindir}/gem
%rb_binary                         %{_bindir}/ruby
%rb_arch                           %(%{rb_binary} -e 'print RUBY_PLATFORM')
%rb_ver                            %(%{rb_binary} -r rbconfig -e 'print RbConfig::CONFIG["ruby_version"]')

## Base
%rb_dir           %(%{rb_binary} -rrbconfig -e 'puts RbConfig::CONFIG["rubylibprefix"]' )
%rb_libdir        %(%{rb_binary} -rrbconfig -e 'puts RbConfig::CONFIG["rubylibdir"]' )
%rb_archdir       %(%{rb_binary} -rrbconfig -e 'puts RbConfig::CONFIG["archdir"]' )

## Site
%rb_sitedir       %(%{rb_binary} -rrbconfig -e 'puts RbConfig::CONFIG["sitedir"]' )
%rb_sitelibdir    %(%{rb_binary} -rrbconfig -e 'puts RbConfig::CONFIG["sitelibdir"]' )
%rb_sitearchdir   %(%{rb_binary} -rrbconfig -e 'puts RbConfig::CONFIG["sitearchdir"]' )

## Vendor
%rb_vendordir     %(%{rb_binary} -rrbconfig -e 'puts RbConfig::CONFIG["vendordir"]' )
%rb_vendorlibdir  %(%{rb_binary} -rrbconfig -e 'puts RbConfig::CONFIG["vendorlibdir"]' )
%rb_vendorarchdir %(%{rb_binary} -rrbconfig -e 'puts RbConfig::CONFIG["vendorarchdir"]' )

# %%gem_unpack macro unpacks a gem file into %%{_builddir}
#
# example:
#   %prep
#   %gem_unpack %{SOURCE0}
#   %patch1 -p1
%gem_unpack(s:) \
  source=%{-s:%{-s*}}%{!-s:%{SOURCE0}} \
  %{gem_binary} unpack --verbose $source \
  cd %{gem_name}-%{version} \
  chmod -Rf a+rX,u+w,g-w,o-w . \
  %{gem_binary} specification --ruby $source > %{gem_name}.gemspec \
%{nil}

# %%gem_build macro ...
%gem_build() \
GEMSPEC_SOURCE_DIR=`find . -maxdepth 2 -type f -name %{gem_name}.gemspec | xargs dirname` \
cd $GEMSPEC_SOURCE_DIR && %{gem_binary} build --verbose %{gem_name}.gemspec \
%{nil}

# %%gem_install macro installs a gem file
#
# example:
#   %install
#   %gem_install my_gem 1.0
%gem_install() \
  cd %{_builddir}/%{gem_name}-%{version} \
  %{gem_binary} install --bindir %{gem_base}/bin/ --build-root %{buildroot} %{gem_name}-%{version}.gem \
%{nil}

%gem_base %(%{rb_binary} -rrubygems -e 'print Gem::Specification.new.base_dir' )
%gem_extensions %(%{rb_binary} -rrubygems -e 'print Gem::Specification.new.extensions_dir' || echo %{_libdir}/ruby/gems/%{rb_ver}/gems )
%gem_platform %(%{rb_binary} -r rubygems -r rbconfig -e 'print Gem::Platform.new(RbConfig::CONFIG["arch"]).to_s' )
