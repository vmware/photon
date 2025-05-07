#! /bin/sh

# linux-api-headers has been excluded from the list of specs to be updated
specs="linux/linux.spec linux/linux-esx.spec linux/linux-rt.spec"

tarball_url=`curl -s https://www.kernel.org  | grep -Eo 'https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.1\.[0-9]*.tar.xz' | uniq`
tarball=$(basename $tarball_url)
version=`echo $tarball | sed 's/linux-//; s/.tar.xz//'`
echo latest linux version: $version
test -f stage/SOURCES/$tarball && echo up to date && exit 0
$(cd stage/SOURCES && wget $tarball_url)
sha512=`sha512sum stage/SOURCES/$tarball | awk '{print $1}'`
changelog_entry=$(echo "`date +"%a %b %d %Y"` `git config user.name` <`git config user.email`> $version-1")
for spec in $specs; do
	sed -i '/^Version:/ s/6.1.[0-9]*/'$version'/' SPECS/$spec
	sed -i '/^Release:/ s/[0-9]*%/1%/' SPECS/$spec
	sed -i '/^%changelog/a* '"$changelog_entry"'\n- Update to version '"$version"'' SPECS/$spec
done
config_tags="-[[:space:]]archive version name url commit_id archive_sha512sum"
config_tags=($config_tags)
for config_tag in "${config_tags[@]:0:4}"; do
	sed -i '0,/^\([[:space:]]*\)'$config_tag':/ s/6.1.[0-9]*/'$version'/' SPECS/linux/config.yaml
done
commit_id=$(git ls-remote --tags https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git v$version^{} | awk '{print $1}')
sed -i '0,/^\([[:space:]]*\)'${config_tags[4]}': [0-9a-z]*$/ s//\1'${config_tags[4]}': '$commit_id'/' SPECS/linux/config.yaml
sed -i '0,/^\([[:space:]]*\)'${config_tags[5]}': [0-9a-z]*$/ s//\1'${config_tags[5]}': '$sha512'/' SPECS/linux/config.yaml
