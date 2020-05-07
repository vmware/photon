#!/usr/bin/perl
#
#                lazyspec © 2020 VMware Inc.,
#
#   Author: Siddharth Chandrasekaran <csiddharth@vmware.com>
#     Date: Thu May  7 00:48:27 IST 2020
#

use Getopt::Long;
use Pod::Usage 'pod2usage';
use File::Basename;
use File::Copy;
use File::Path;
use HTTP::Tiny;
use File::Temp 'tempfile';
use POSIX 'strftime';
use Cwd 'abs_path';
use Digest::file 'digest_file_hex';
use Data::Dumper;
use File::Find;

=head1 NAME

  lazyspec.pl - A tool for the truly lazy SPEC file maintainer

=head1 SYNOPSIS

  lazyspec.pl [OPTIONS] [SPEC1 [SPEC2, ...]]

=head1 DESCRIPTION

  lazyspec.pl is a script that allows automation of some common work-flows done on a SPEC file.

  It can automate the following actions:
    1. Adding a patch to fix CVEs in packages.
    2. Adding changelog and updating release numbers.
    3. Updating package versions.

  In addition, it can also,
    1. Check if all patches to a SPEC file can be applied.
    2. Make source tree out of a SPEC file.

=head1 OPTIONS

  -c, --cve CVE_NUMBER      CVE number for the issue being fixed. This is used to produce the patch
                            file name (unless, --keep-names is specified). It is also used to auto
                            generate changelog message (unless --message is provided) and comment
                            above the patch source entry.
  -p, --patch PATH          Path to patch file. Alternatively, a URL to patch file (raw) can also be
                            passed.
  -u, --upgrade-to VERSION  Upgrade spec file to VERSION. Must pass --source along with this option.
                            When this option is set to "latest", lazyspec will try to upgrade to the
                            latest version of that package. Currently, "latest" works only on
                            kernels.
  -s, --source PATH         Path to source tarball. Alternatively, a URL to the tarball can also be
                            passed.
  -m, --message MESSAGE     String that goes into the changelog entry of the spec file (also updates
                            release number). This can be handy if you have done some modifications
                            (manually), and just want to increment the release and put a changelog
                            entry.
  --kernels                 Instruct to perform some kernel spec specific optimizations. Also, when
                            this flag is passed, all kernel spec files are considered (instead of
                            having to pass them individually).
  --keep-names              Preserve patch file names (defaults to CVE-NUMBER.patch)
  --check                   Check the given spec files to see if all its patches (current) can be
                            applied on its source. This will also try to guess if a patch is made
                            redundant (already incorporated) in current source tarball. This is
                            useful soon after a --upgrade-to action especially in packages that have
                            many patches with frequent upgrades such as in the kernels.
  --make-tree               Create a source tree based on the details extracted from the spec file.
                            The source tree produced, resides in /tmp and includes all patches
                            applied by that spec file. This command can operate only on one spec
                            file at a time.
  --man                     Display the full man page for this tool.
  -h, --help                Print a short help text.

=head1 EXAMPLES

    1. Apply a patch from github to a spec file

        lazyspec.pl --cve CVE-2020-12345 \
                    --patch https://github.com/yarnpkg/yarn/commit/62aec83ed84cc20cc6edbf17e4c518ee1dfd16af.patch \
                    SPECS/yarn/yarn.spec

    2. Add changelog to any package:

        lazyspec.pl --message "This text will appear in the changelog" \
                    SPEC/iptables/iptables.spec

    3. Add a patch to all kernels:

        lazyspec.pl --cve CVE-2020-12345 \
                    --patch kvm-dont-accept-wrong-gsi-values.patch \
                    --kernels --keep-names

    4. Upgrade kernels to latest version

        lazyspec.pl --upgrade-to latest --kernels

    5. Upgrade kernels to a specific version

        lazyspec.pl --upgrade-to 4.19.121 \
                    --source https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.19.121.tar.xz \
                    --kernels

    6. Check patches to a package:

        lazyspec.pl --check --kernels
        lazyspec.pl --check SPECS/kubernetes/kubernetes-1.14.spec

    7. Created a source tree for a package with all its patches applied:

        lazyspec.pl --make-tree SPEC/linux/linux-rt.spec

=head1 BUGS

  Due to the nature of problem this tool tries to solve, be warned that there can be issues when run
  on an arbitrary SPEC file. Report bugs identified to the MAINTAINERS.

=head1 MAINTAINERS

  Siddharth Chandrasekaran <csiddharth@vmware.com>

=head1 VERSION

  1.0.0

=cut

GetOptions (
  'cve=s'         => \my $cve_number,
  'upgrade-to=s'  => \my $upgrade_to,
  'source=s'      => \my $source_tarball,
  'patch=s'       => \my $patch_file,
  'message=s'     => \my $change_log,
  'kernels'       => \my $flag_kernels,
  'keep-names'    => \my $flag_keep_names,
  'check'         => \my $flag_check,
  'make-tree'     => \my $flag_make_tree,
  'man'           => sub { pod2usage(VERBOSE => 2) },
  'help'          => sub { pod2usage(1) },
);

my @spec_files = @ARGV;

if (defined $flag_kernels) {
    @spec_files = glob 'SPECS/linux/linux*.spec';

    # if we are updating and the target package being upgraded is kernels
    # add the linux-api-headers.spec to spec file list
    if (defined $upgrade_to) {
        push(@spec_files, 'SPECS/linux-api-headers/linux-api-headers.spec');
    }
}

if (scalar @spec_files == 0) {
    die "Must provide a spec file to operate on\n";
}

if (defined $flag_make_tree) {
    die ("Error: Cannot make-tree on multiple spec files\n") if (scalar @spec_files > 1);
    print("Building source tree for $spec_files[0]\n");
    spec_make_source_tree($spec_files[0], 1);
    exit;
}

if (defined $flag_check) {
    foreach(@spec_files) {
        print("Checking: $_\n");
        spec_make_source_tree($_);
    }
    exit;
}

if (defined $cve_number and not defined $patch_file) {
    die "Error: Must provide patch file (--patch) when --cve is passed\n";
}

if (defined $patch_file and defined $source_tarball) {
    die "Error: cannot patch and upgrade version at the same time\n";
}

if (defined $upgrade_to) {
    if ($upgrade_to =~ /^latest$/ and defined $flag_kernels) {
        %rel = kernel_org_get_releases();
        %meta = spec_get_metadata("SPECS/linux/linux.spec");
        $upgrade_to = $rel{ $meta{ 'rel_tree' } }{ 'version' };
        if ($upgrade_to eq $meta{'rel_version'}) {
            die "Already at latest kernel release $upgrade_to.\n";
        }
        $source_tarball = $rel{ $meta{ 'rel_tree' } }{ 'source' };
    }
    die "Error: --source must be passed to upgrade version.\n" unless(defined $source_tarball);
    if ($source_tarball =~ /^https?:\/\//) {
        $file = (split(/\//, $source_tarball))[-1];
        if (not -f "stage/SOURCES/".$file) {
            die("Can't write to state/SOURCES/\n") if( not -w "state/SOURCES/");
            print("Fetching source tarball from $source_tarball\n");
            $tmp = download_file($source_tarball);
            move($tmp, "stage/SOURCES/".$file);
            chmod(0644, "stage/SOURCES/".$file);
        } else {
            print("Using existing source tarball\n");
        }
    } else {
        $file = basename($source_tarball);
        if (not -f "stage/SOURCES/".$file) {
            die("Can't write to state/SOURCES/\n") if( not -w "state/SOURCES/");
            move($source_tarball, "stage/SOURCES/".$file);
            chmod(0644, "stage/SOURCES/".$file);
        } else {
            print("Using existing source tarball\n");
        }
    }
    $source_tarball = "stage/SOURCES/".$file;
    $source_sha = `sha1sum $source_tarball`;
    $source_sha =~ s/^(\w+)\s.*/$1/;
    print("Source tarball sha: $source_sha\n");
}

if (not defined $change_log and (defined $cve_number or defined $upgrade_to)) {
    print("Warning: auto generating changelog!\n");
    if (defined $cve_number) {
        $change_log = "Add patch to fix ".$cve_number;
    } else {
        $change_log = "Update to version $upgrade_to";
    }
}

if ($patch_file =~ /^https?:\/\//) {
    die "Error: Must pass --cve when patch is a URL!\n" unless(defined $cve_number);
    print("Fetching patch file... ");
    $patch_file = download_file($patch_file);
    print("Done.\n");
}

if (not defined $change_log) {
    die "Error: --message not provided and was not able to auto determine\n".
        "it. See --help for more details\n";
}

$spec_base = dirname(abs_path($spec_files[0]));
if (defined $cve_number) {
    die "Error: invalid patch file $patch_file\n" unless(-f $patch_file);
    if (dirname(abs_path($patch_file)) ne $spec_base) {
        if (defined $flag_keep_names) {
            $patch_file_name = basename($patch_file);
        } else {
            $patch_file_name = $cve_number.".patch";
        }
        if (-f $spec_base.'/'.$patch_file_name) {
            die "Error: Patch file $patch_file_name already applied\n";
        }
        copy($patch_file, $spec_base.'/'.$patch_file_name);
        $patch_file = $patch_file_name;
        print("Copied patch $patch_file_name to $spec_base.\n");
    }
}

print("\n");

sub spec_make_source_tree {
    my $spec = shift;
    my $keep = shift;
    my $patch_failed = 0;
    my $tmp_dir = File::Temp->newdir;
    my %meta = spec_get_metadata($spec);
    # print Dumper(\%meta);
    my %result;
    $result{ 'obsolete' } = ();
    $result{ 'failed' } = ();

    # when upgrading, dont consider version from the spec file.
    # The spec file version is used to build current tree (which
    # is the case when --make-tree is passed.)
    if (defined $upgrade_to) {
        $version = $upgrade_to;
    } else {
        $version = $meta{'rel_version'}
    }

    @tarball = glob 'stage/SOURCES/'.$meta{'name'}.'-'.$version.'*';
    if (scalar @tarball != 1) {
        die("Error: Could not locate a source tarball for $meta{'name'}-$version\n");
    }
    print("  Extracting $tarball[0] at $tmp_dir\n");
    qx{ tar xf $tarball[0] -C $tmp_dir --strip-components=1 };
    die("Error: Failed to untar $tarball[0].\n") if ($? != 0);
    foreach $tuple (@{ $meta{ 'patches' } }) {
        $patch_number = @{$tuple}[0];
        $patch = @{$tuple}[1];
        $patch_level = @{$tuple}[2];

        # Hacky, but works (??). Try to revert each patch and see
        # if that succeeds. If it does, then this patch _can_ be
        # removed. There can be false positives, especally when
        # the patch context is too low.
        qx { patch -d $tmp_dir -R -p$patch_level -sf --dry-run < $patch };
        if ($? == 0) {
            print("  Skip: Patch$patch_number: $patch\n");
            push(@{ $result{ "obsolete" } }, [$patch_number, $patch]);
            next;
        }

        # So far so good. Try to apply the patch.
        # print("APPLY: $patch\n");
        @stdout = qx{ patch -d $tmp_dir -p$patch_level -f < $patch };
        if ($? != 0) {
            print("  Error: Patch$patch_number: $patch failed. Error code: $?\n");
            print("  > $_") foreach (@stdout);
            push(@{ $result{ "failed" } }, [$patch_number, $patch]);
            $patch_failed = 1;
        }
    }

    if ($patch_failed or (defined $keep and $keep)) {
        $keep_path = '/tmp/'.$meta{'package_name'}.'-'.$version;
        rmtree($keep_path) if (-d $keep_path);
        move($tmp_dir, $keep_path);
        print("  Source tree preserved at: $keep_path\n");
    }
    return %result;
}

sub find_patch {
    my $dirpath = shift;
    my $patch = basename(shift);
    my @files;
    find(sub {
             return unless -f;
             return if (index($_, $patch) == -1);
             push @files, $File::Find::name;
         },
         $dirpath
    );
    if (scalar @files == 0) {
        print("Warning: unable to find patch file $patch. Skipped.\n");
        return undef;
    }
    print("Matched more than one patch file for $patch\n") if (scalar @files > 1);
    return $files[0];
}

sub spec_get_metadata {
    my %meta;
    my $spec = shift;
    $spec_base = dirname($spec);
    $meta{ "name" } = basename($spec_base);
    open(FH, "<", $spec) // die "Error: failed to open $spec\n";
    $meta{ "patches" } = ();
    %patch_files;
    while (<FH>) {
        if (/^Name:\s+(\S+)/) {
            $meta{ "package_name" } = $1;
        }
        if (/^Version:\s+((\d+\.\d+)\.\d+)/) {
            $meta{ "rel_version" } = $1;
            $meta{ "rel_tree" } = $2;
        }
        if (/^Patch(\d+):\s+(\S+)$/) {
            $patch = find_patch($spec_base, $2);
            $patch_files{ $1 } = $patch;
        }
        push (@{ $meta{ "patches" } }, [$1, "", $2]) if (/^%patch(\d+)\s+-p(\d+)/);
    }
    close(FH);
    foreach (@{ $meta{ "patches" } }) {
        @{$_}[1] = $patch_files{@{$_}[0]};
    }
    return %meta;
}

sub kernel_org_get_releases {
    my $response = HTTP::Tiny->new->get("https://www.kernel.org/");
    die "Failed to reach kernel.org\n" unless $response->{success};

    print("Fetching latest releases from https://www.kernel.org\n");
    my @links = $response->{content} =~ /href="(https:\/\/[^<>\s]+)"/g;
    my %rel;
    foreach (@links) {
        if (($full_version, $short_version) = /linux-((\d+\.\d+)\.\d+)\.tar/) {
            $rel{ $short_version }{ 'version' } = $full_version;
            $rel{ $short_version }{ 'source' } = $_ if (/\.tar\.xz$/);
            $rel{ $short_version }{ 'signature' } = $_ if (/\.tar\.sign$/);
        }
    }
    return %rel;
}

sub download_file {
    $url = shift;
    my $response = HTTP::Tiny->new->get($url);
    die "Failed to fetch $url\n" unless $response->{success};

    ($fh, $filename) = tempfile();
    #binmode($fh, ":utf8");
    print($fh $response->{content}) if length $response->{content};
    close($fh);
    return $filename;
}

sub read_lines {
    ($file) = @_;

    open(FH, "<", $file) // die "Error: Unable to open $file for read\n";
    @lines = <FH>;
    close(FH);
    return @lines
}

sub write_lines {
    ($file, $ref_lines) = @_;
    @lines = @{$ref_lines}; # dereference

    open(FH, ">", $file) // die "Error: Unable to open $file for write\n";
    foreach $line ( @lines ) {
        print FH $line
    }
    close(FH);
}

sub spec_add_patch {
    $lines = shift;
    $state = "SETUP";
    ($vr_done, $rl_done, $sha_done) = (0, 0, 0);
    ($slot_found, $slot_pos) = (0, 0);

    print("Fixup spec file $spec\n");
    for ($i=0; $i <= $#$lines; $i++) {
        $_ = $lines->[$i];

        # The goal of this state is to wait for a pattern
        # and then move to the next_state as requested by
        # the caller of this state. Nothing Fancy.
        if ($state eq "WAIT_FOR_PATTERN") {
            next unless ($_ =~ $pattern);
            $state = $next_state;
        }

        # We try to get the version and release from the
        # head of the spec file.
        if ($state eq "SETUP") {
            if (defined $upgrade_to) {
                $name = $1 if (/^Name:\s+(\w+).*$/);
                if (/^Version:/) {
                    $lines->[$i] =~ s/^(Version:\s+)[0-9.]+$/$1$upgrade_to/;
                    $vr_done = 1;
                }
                if (/^Release:/) {
                    $lines->[$i] =~ s/^(Release:\s+)(\d+)(.*)$/${1}1${3}/;
                    $rl_done = 1;
                }
                if (/^%define\s+sha1\s+$name=/) {
                    $lines->[$i] =~ s/^(%define\s+sha1\s+$name=).*$/$1$source_sha/;
                    $sha_done = 1;
                }
                next unless($vr_done and $rl_done and $sha_done);
                $rel = 1;
                $ver = $upgrade_to;
                ($pattern, $next_state) = (qr/^%changelog/, "CHANGE_LOG");
                $state = "WAIT_FOR_PATTERN";
            } else {
                $ver = $1 if (/^Version:\s+([0-9.]+)$/);
                if (/^Release:(\s+)(\d+)(.*)/) {
                    $rel = $2 + 1;
                    print("Updating release number..\n");
                    splice @$lines, $i, 1, "Release:$1$rel$3\n";
                } else { next }
                # Wait till we hit the first Patch entry
                if (defined $patch_file) {
                    # When a patch file is defined, we must move to the FIND_SLOT
                    # state. The only catch is that, if the package being upgraded,
                    # is kernels, we have too many empty slots to pick from and we
                    # shouldn't pick the first available slot. So we wait for the
                    # first occurrence of "# Fix for CVE-" and then pick the next
                    # free slot.
                    if (defined $flag_kernels) {
                        $pattern = qr/^# Fix for CVE-/;
                        $next_state = "FIND_SLOT";
                        $state = "WAIT_FOR_PATTERN";
                    } else {
                        $state = "FIND_SLOT";
                    }
                } else {
                    $pattern = qr/^%changelog/;
                    $next_state = "CHANGE_LOG";
                    $state = "WAIT_FOR_PATTERN";
                }
            }
        }

        # In this state, we try to locate the lowest unused
        # patch number (slot). Here we keep track of previous
        # slot number and check if there are any gaps to add
        # this patch. If no such slot is found, the patch is
        # added as the last slot.
        elsif ($state eq "FIND_SLOT") {
            $patch_zero = $i if (/^(Distribution:|Build)/);
            ($current) = /^Patch(\d+):/;
            ($last, $ws) = $lines->[$slot_pos] =~ /^Patch(\d+):(\s+)/;

            if (defined $current and not defined $last) {
                # we try to maintain $last with a good slot position.
                # if we see current and no last, then this is the first
                # time we are entering this section.
                $slot_pos = $i;
            }
            elsif (not defined $last and /^%/ and not /^%(define|global)/) {
                # we got to a non %define and non %global %* entry
                # while still not identifying last. This means
                # there was no patch entry in the spec. Since we
                # are going to enter the first patch entry, we will
                # do it after the last seen of Distribution or Build*
                # sections.
                $slot_found = 1;
                $slot_pos = $patch_zero;
                $patch_no = 0;
            }
            elsif (defined $last and not defined $current and
                not /^(\s+)?$/ and not /^#/) {
                # not an empty line, not a comment, not a Patch* too.
                # This means we walked out of the patch source region
                # so we can safely use the last seen patch number + 1
                # as slot.
                $slot_found = 1;
                $patch_no = $last + 1;
            }
            elsif (defined $last and defined $current and
                $last + 1 < $current) {
                # this is straightforward, there is a discontinuity in
                # in the patch numbers. Choose $last + 1 as slot.
                $slot_found = 1;
                $patch_no = $last + 1;
            } else {
                # Failed very case. so we update last if needed and move
                # to next offset.
                $slot_pos = $i if (defined $current);
            }
            next unless($slot_found);

            # found first empty slot or last patch source entry
            # insert the 2 new lines and move to next state.
            print("Adding patch source entry at slot ", $patch_no+1, "\n");
            @new = ();
            push(@new, "# Fix for $cve_number\n") if (defined $cve_number);
            push(@new, "Patch$patch_no:".$ws."$patch_file\n");
            splice @$lines, $slot_pos+1, 0, @new;

            # Wait till we reach the prep section
            ($pattern, $next_state) = (qr/^%prep/, "APPLY_PATCH");
            $state = "WAIT_FOR_PATTERN";
        }

        # In the prep section, we wait for the same slot
        # number that was identified in FIND_SLOT and add
        # an entry to apply that patch.
        elsif ($state eq "APPLY_PATCH") {
            # skip any %setup %if %endif tags
            next if (/^%(setup|if|endif)/);

            ($current) = /^%patch(\d+)/;

            # if patch_no is 0 we must put the entry in %prep
            # after all %setup tags. If that is not the case,
            # we can also skip any patch up until we git target
            # patch ($patch_no).
            if ($patch_no != 0 and (not defined $current or
                $current + 1 != $patch_no)) {
                next;
            }

            # insert the "%patchXX -p1" line
            print("Adding patch apply entry in %prep section.\n");
            splice @lines, $i+1, 0, "%patch$patch_no -p1\n";

            # Wait till we reach the changelog section
            ($pattern, $next_state) = (qr/^%changelog/, "CHANGE_LOG");
            $state = "WAIT_FOR_PATTERN";
        }

        # Last, update the changelog section. This is the last
        # phase and the loop exits early as there is no need to
        # look at older change logs.
        elsif ($state eq "CHANGE_LOG") {
            next if(/^%changelog/);
            # to handle inconsistent whitespace in change log,
            # we try copy the last used white space. Perhaps we should
            # just fix all whitespace in one shot with a perl -i -pe ''?
            print("Updating changelog with message: $change_log\n");
            ($ws) = /^\*(\s+)/;
            $date = strftime("%a %b %d %Y", localtime);
            chomp($name=`git config user.name`);
            chomp($email=`git config user.email`);
            @new = ("*".$ws."$date $name <$email> $ver-$rel\n",
                    "-".$ws."$change_log\n");
            splice @$lines, $i, 0, @new;
            last; # exit early
        }
    }
    print("\n");
    if ($state ne "CHANGE_LOG") {
        die "Did not reach CHANGE_LOG state.\nCurrent state: $state\n";
    }
}

foreach $spec ( @spec_files ) {
    @lines = read_lines($spec);
    spec_add_patch(\@lines);
    # Write back the modified lines into file
    write_lines($spec, \@lines);
}
