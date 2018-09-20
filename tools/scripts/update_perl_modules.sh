#!/bin/sh
PROG=$0                                   # The script name
PERL_PACKAGE_LIST=""                      # List of spec directories of perl packages
tmpJsonFile=$(mktemp /tmp/perl.XXXXXXXXX) # Temporary file to hold package json
perlModuleName=""                         # Name of the current perl module
srcUrl=""                                 # Source code URL
latestVersion=""                          # Package version number
SPECSDIR=SPECS                            # Parent directory of  all SPEC files
SOURCESDIR="stage/SOURCES"                # Directory where sources are downloaded
latestSrcFileName=""                      # Base name of source file
srcSha1Sum=""                             # sha1sum of the sources
changeMsgLine1=""                         # first line of the changelog message to record
changeMsgLine2=""                         # second line of the changelog message to record

function _help()
{
    echo "
Usage: $PROG [--help|-h]

Run the script from git workspace root of photon where .git directory exists.
This script upgrades the Perl modules used in Photon to their latest versions.
"
    exit ${1:-0}
}

function _isRunningFromGitWorkspace()
{
    local folderName
    local rc=0

    for folderName in .git SPECS
    do
        if [ ! -d ".git" ]
        then
            rc=$?
            echo "Expected directory $folderName does not exist." \
                 "Please run this script from git workspace of Photon."
            return $rc
        fi
    done
    return $rc
}
################################################################################
# Converts spec dir name of a Perl package to a module name
#
# Usage: _specDirToPackageName perl-DBIx-Simple
# Sample output : DBIx::Simple
################################################################################
function _specDirToPackageName()
{
    echo "$1" | cut -d '-' -f 2- | sed -e 's/-/::/g'
}


################################################################################
# Gets the Json of package information from metacpan.org
#
# Usage: _downloadJsonForPackage <package-name> ## example, "DBIx::Simple"
# Sample output :
# {
#   "date" : "2017-12-08T22:54:24",
#   "download_url" : "https://cpan.metacpan.org/authors/id/J/JU/JUERD/DBIx-Simple-1.37.tar.gz",
#   "status" : "latest",
#   "version" : "1.37"
# }
################################################################################
function _downloadJsonForPackage()
{
    curl -s "http://fastapi.metacpan.org/v1/download_url/$1" > $tmpJsonFile
}

################################################################################
# Downloads a source archive from provided url and store as target file name
#
# Usage: _downloadSourceFromUrl <source-archive-url> <target-download-path>
################################################################################
function _downloadSourceFromUrl()
{
    local fromUrl="$1"
    local toFile="$2"
    curl -s "$fromUrl" > "$toFile"
}

################################################################################
# Update spec file with provided parameters
#
# Usage: _updateSpecFile <spec-file> <version> <url> <localSourceFile>
#                        <changelog-firstline> <changelog-secondline>
################################################################################
function _updateSpecFile()
{
    local specFile="$1"
    local latestVersion="$2"
    local srcUrl="$3"
    local localSrcArchive="$4"
    local changeLogMsg1="$5"
    local changeLogMsg2="$6"
    local sha1sum=""
    local existingVersion=""
    local downloadUrl="$(echo $srcUrl | sed -E "s/$latestVersion/%{version}/g")"
    downloadUrl="$(echo "$downloadUrl" | sed -E 's#/#\\/#g')"
    _downloadSourceFromUrl "$srcUrl" "$localSrcArchive"
    sha1sum="$(sha1sum $localSrcArchive | awk '{print $1}')"

    existingVersion="$(awk '/^Version:/{print $2}' $specFile)"

    if [ "$existingVersion" == "$latestVersion" ]
    then
        echo "$specFile is already at latest version $latestVersion. Skipping..."
        return 0
    fi
    echo -n "Upgrading spec file $specFile to $latestVersion from $existingVersion..."

    # Update %version
    sed -i -e "s/^\(Version:[[:space:]]*\)[^[:space:]].*$/\1$latestVersion/" $specFile

    # Update %release
    sed -i -e "s/^\(Release:[[:space:]]*\)[^[:space:]]*%\(.*\)$/\11%\2/" $specFile
    
    # Update %Source/%Source0
    sed -i -e "s/^\(Source[0]*:[[:space:]]*\).*$/\1$downloadUrl/" $specFile

    # Update sha1sum
    sed -i -e "s/^\(%define[[:space:]]\+sha1.*\)=.*$/\1=$sha1sum/" $specFile

    # Update changelog
    sed -i -e "/^%changelog/a\
              $changeLogMsg1" $specFile
    sed -i -e "/$changeLogMsg1/a\
              $changeLogMsg2" $specFile
    echo "Done"
}

if [ $# -gt 1 ]
then
    _help 1
elif [ $# -eq 1 ]
then
    echo "$1" | grep -q -E -- '(^--help$)|(^-h$)' && _help 0
    echo "Invalid option '$1'" 1>&2
    _help 1
fi
# exit if not running from git workspace of Photon
_isRunningFromGitWorkspace || _help $?
PERL_PACKAGE_LIST="$(find SPECS/ -type d -name 'perl-*' -exec basename {} \;)"
mkdir -p "$SOURCESDIR"
for p in $PERL_PACKAGE_LIST
do
    perlModuleName="$(_specDirToPackageName $p)"
    _downloadJsonForPackage "$perlModuleName"
    while read line
    do
        if echo $line | grep -q '"download_url"'
        then
            srcUrl="$(echo \"$line\" | cut -d ':' -f 2- | sed -e 's/[,\" ]//g')";
            continue
        fi
        if echo $line | grep -q '"version"'
        then
            latestVersion="$(echo \"$line\" | cut -d ':' -f 2- | sed -e 's/[,\" ]//g')";
            continue
        fi
    done < $tmpJsonFile
    latestSrcFileName="$(basename $srcUrl)"
    changeMsgLine1="$(echo -e "*   $(date '+%a %b %d %Y') Dweep Advani <$(git config --get user.email)> $latestVersion-1\n")"
    changeMsgLine2="$(echo -e "-   Update to version $latestVersion\n")"
    _updateSpecFile "$SPECSDIR/$p/$p.spec" \
                    "$latestVersion" \
                    "$srcUrl" \
                    "$SOURCESDIR/$latestSrcFileName" \
                    "$changeMsgLine1" \
                    "$changeMsgLine2"
done
rm -f $tmpJsonFile
