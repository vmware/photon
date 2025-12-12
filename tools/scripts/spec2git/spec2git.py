#!/usr/bin/env python3
"""
RPM Spec to Git Repository Converter (and Git to Spec Converter)

This script provides bidirectional conversion between RPM .spec files and git repositories.

Usage:
    ./spec2git.py <spec_file> [options]

For SPEC TO GIT conversion:
    ./spec2git.py linux.spec
    ./spec2git.py linux.spec --output-dir /tmp/linux-git

For GIT TO SPEC conversion:
    ./spec2git.py linux.spec --git2spec --git-repo /tmp/linux-git

Author: Generated for Photon OS development
License: Apache 2.0
"""

import argparse
import logging
import sys
import os

# Add current directory to path for local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from local modules
from spec2git_lib.spec2git_main import Spec2Git
from git2spec.git2spec_core import Git2Spec
from common.exceptions import ValidationError


def setup_logging(verbose: bool) -> None:
    """Configure logging for the application"""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def main() -> int:
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Convert between RPM spec files and git repositories (bidirectional)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
SPEC TO GIT Examples:
  %(prog)s linux.spec
  %(prog)s linux.spec --output-dir /tmp/linux-git
  %(prog)s linux.spec --define canister_build=1
  %(prog)s linux.spec --stop-before-patch Patch512
  %(prog)s linux.spec --use-tarball
  %(prog)s linux.spec --use-git-apply

GIT TO SPEC Examples:
  %(prog)s linux.spec --git2spec --git-repo /tmp/linux-git
  %(prog)s linux.spec --git2spec --git-repo /tmp/linux-git --output-spec new.spec
  %(prog)s linux.spec --git2spec --git-repo /tmp/linux-git --changelog "Fixed CVE"
  %(prog)s linux.spec --git2spec --git-repo /tmp/linux-git --use-commit-messages
        """
    )

    parser.add_argument('spec_file', help='Path to the .spec file')
    parser.add_argument('--git2spec', action='store_true',
                       help='Convert git repository back to spec file')

    # Spec2Git options
    parser.add_argument('--output-dir', '-o',
                       help='[spec2git] Output directory for git repository')
    parser.add_argument('--define', '-D', action='append', dest='macros',
                       help='[spec2git] Define macro (format: name=value or name)')
    parser.add_argument('--stop-before-patch',
                       help='[spec2git] Stop before applying patch (e.g., "Patch512" or "512")')
    parser.add_argument('--resume', action='store_true',
                       help='[spec2git] Resume execution from saved state (use after resolving conflicts, or after --stop-before-patch)')
    parser.add_argument('--use-tarball', action='store_true',
                       help='[spec2git] Force using tarball instead of git repository')
    parser.add_argument('--force', '-f', action='store_true',
                       help='[spec2git] Force overwrite existing output directory')
    parser.add_argument('--use-git-apply', action='store_true',
                       help='[spec2git] Use "git apply" instead of "patch" command')

    # Git2Spec options
    parser.add_argument('--git-repo',
                       help='[git2spec] Path to git repository with changes')
    parser.add_argument('--output-spec',
                       help='[git2spec] Output spec file path (default: overwrite original)')
    parser.add_argument('--changelog',
                       help='[git2spec] Custom changelog message')
    parser.add_argument('--use-commit-messages', action='store_true',
                       help='[git2spec] Use commit messages for changelog')

    # Common options
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--arch',
                       help='Target architecture (e.g., x86_64, aarch64)')

    args = parser.parse_args()
    setup_logging(args.verbose)

    try:
        if args.git2spec:
            # Git to Spec mode
            if not args.git_repo:
                parser.error("--git-repo is required when using --git2spec")

            converter = Git2Spec(
                spec_file=args.spec_file,
                git_repo_dir=args.git_repo,
                output_spec=args.output_spec,
                changelog_msg=args.changelog,
                use_commit_msgs=args.use_commit_messages,
                verbose=args.verbose
            )
            success = converter.run()
        else:
            # Spec to Git mode (default)
            macros = {}
            if args.macros:
                for macro_def in args.macros:
                    if '=' in macro_def:
                        name, value = macro_def.split('=', 1)
                        macros[name] = value
                    else:
                        macros[macro_def] = '1'

            converter = Spec2Git(
                spec_file=args.spec_file,
                output_dir=args.output_dir,
                macros=macros,
                stop_before_patch=args.stop_before_patch,
                resume=args.resume,
                verbose=args.verbose,
                use_tarball=args.use_tarball,
                force=args.force,
                target_arch=args.arch,
                use_git_apply=args.use_git_apply,
                cmd_str=' '.join(sys.argv[0:]),
            )
            success = converter.run()

        return 0 if success else 1

    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        return 1
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
