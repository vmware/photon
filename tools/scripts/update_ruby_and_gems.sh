#! /bin/sh

ruby_spec="ruby/ruby.spec"

if [ ! -d ./SPECS/ ]; then
  echo "This script has to be executed from git photon working directory"
fi

tarball_url=`curl -s https://www.ruby-lang.org/en/downloads/ | grep -E "The current stable version is"`
tarball="https://cache.ruby-lang.org/pub/ruby"
version=`echo $tarball_url | sed -e 's/The current stable version is //' | cut -c1-5`

#Set the ENV accordingly to export the path of rvm installed
export PATH=$PATH:/home/srinidhir/.rvm/rubies/ruby-2.5.1/bin

gem_bin=`which gem`
if [ -z $gem_bin ]; then
  echo "Gem not found"
  echo "Please install ruby and gem using rvm"
  echo "Please follow this link to install https://www.digitalocean.com/community/tutorials/how-to-install-ruby-and-set-up-a-local-programming-environment-on-ubuntu-16-04"

else

  echo "gem is installed"

fi

echo latest ruby version: $version

major_ver=`echo $version | cut -c1-3`

tar_url="$tarball/$major_ver/ruby-$version.tar.bz2"
ruby_tar="ruby-$version.tar.bz2"

old_ruby_ver=`grep -m 1 -w "Version:" ./SPECS/$RUBY_SPEC | sed -e 's/^\(.*\)Version://' | tr -s " "`

if [ "$version" != "$old_ruby_ver" ]; then

  #test -f stage/SOURCES/ruby-$version* && echo up to date && exit 0
  $(cd stage/SOURCES && wget $tar_url)
  sha1=`sha1sum stage/SOURCES/$ruby_tar | awk '{print $1}'`
  echo $sha1
  changelog_entry=$(echo "`date +"%a %b %d %Y"` `git config user.name` <`git config user.email`> $version-1")

  sed -i '/^Version:/ s/2.[0-9]*.[0-9]*/'$version'/' ./SPECS/ruby/ruby.spec
  sed -i '/^Release:/ s/[0-9]*%/1%/' ./SPECS/ruby/ruby.spec
  sed -i '/^%define sha1\s*ruby/ s/=[0-9a-f]*$/='$sha1'/' ./SPECS/ruby/ruby.spec
  sed -i '/^%changelog/a*   '"$changelog_entry"'\n-   Update to version '"$version"'' ./SPECS/ruby/ruby.spec

else
  
  echo "Ruby is up to date"

fi

rubygem_download_url="https://rubygems.org/downloads"

gem_specs_dirs=`find ./SPECS/ -maxdepth 1 -type d -name rubygem-* -exec basename {} \;`
gem_spec_dirs=`find ./SPECS/ -maxdepth 1 -type d -name rubygem-* -exec basename {} \;`

for dir in $gem_spec_dirs; do
  file=`find ./SPECS/$dir/*.spec`
  #Extract name, version and url of the gem.
  #Name is very important
  gem_name=`grep -m 1 -w "gem_name" $file | sed -e 's/^\(.*\)gem_name //'`
  old_ver=`grep -m 1 -w "Version:" $file | sed -e 's/^\(.*\)Version://' | tr -s " "`
  echo "Old version is $old_ver"

  new_ver=`gem search -e $gem_name -r -d | grep -m 1 -w "$gem_name" | sed -e "s/$gem_name (//; s/.$//" | cut -d , -f1`

  echo "Got $gem_name-$new_ver"
  ##gem fetch $gem_name-$new_ver

  gem_exists="./stage/SOURCES/$gem_name-$new_ver*"

  if [ $new_ver != $old_ver ]; then

    echo "updating $gem_name-$new_ver"

    $(cd stage/SOURCES && wget $rubygem_download_url/$gem_name-$new_ver.gem)
    gem_sha1=`sha1sum stage/SOURCES/$gem_name-$new_ver.gem | awk '{print $1}'`
    echo "$gem_sha1"
    gem_chng_log=$(echo "`date +"%a %b %d %Y"` `git config user.name` <`git config user.email`> $new_ver-1")

    sed -i '/^Version:/ s/[0-9].[0-9]*.[0-9]*..$/'$new_ver'/' $file
    sed -i '/^Release:/ s/[0-9]*%/1%/' $file
    sed -i '/^%define sha1\s*'"$gem_name"'/ s/=[0-9a-f]*$/='$gem_sha1'/' $file
    sed -i '/^%changelog/a*   '"$gem_chng_log"'\n-   Update to version '"$new_ver"'' $file

  else

    echo "Gem $gem_name is up to date $new_ver"

  fi

done
