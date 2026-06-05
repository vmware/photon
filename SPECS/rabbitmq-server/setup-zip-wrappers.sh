#!/bin/bash
# zip and unzip are deprecated in Photon 5.0+.
# This script creates lightweight Python-based wrappers for both tools and
# prepends their directory to PATH so that build scripts can locate them.

_jdk_tools_dir=$(mktemp -d /tmp/jdk-tools.XXXXXX)

cat > "$_jdk_tools_dir/unzip" << 'PYEOF'
#!/usr/bin/env python3
import sys, zipfile, os
args, outdir, zippath, i = sys.argv[1:], ".", None, 0
while i < len(args):
    if args[i] in ('-q', '-o', '-n', '-u', '-j', '-a', '-l', '-v', '-p', '-x'):
        i += 1
    elif args[i] == '-d' and i + 1 < len(args):
        outdir = args[i + 1]; i += 2
    elif not args[i].startswith('-') and zippath is None:
        zippath = args[i]; i += 1
    else:
        i += 1
if zippath:
    if not os.path.exists(zippath) and not zippath.endswith('.zip'):
        zippath += '.zip'
    with zipfile.ZipFile(zippath) as zf:
        zf.extractall(outdir)
PYEOF
chmod +x "$_jdk_tools_dir/unzip"

cat > "$_jdk_tools_dir/zip" << 'PYEOF'
#!/usr/bin/env python3
import sys, zipfile, os
args, outpath, files, recursive, read_stdin, store_only, i = sys.argv[1:], None, [], False, False, False, 0
while i < len(args):
    a = args[i]
    if a.startswith('-'):
        if 'r' in a or 'R' in a: recursive = True
        if '0' in a: store_only = True
        if '@' in a: read_stdin = True
        i += 1
    elif outpath is None:
        outpath = a; i += 1
    else:
        files.append(a); i += 1
if read_stdin:
    for line in sys.stdin:
        line = line.rstrip('\n')
        if line: files.append(line)
if outpath:
    compression = zipfile.ZIP_STORED if store_only else zipfile.ZIP_DEFLATED
    mode = 'a' if os.path.exists(outpath) else 'w'
    with zipfile.ZipFile(outpath, mode, compression) as zf:
        for f in files:
            arcname = f[2:] if f.startswith('./') else f
            if os.path.isfile(f):
                zf.write(f, arcname)
            elif os.path.isdir(f) and recursive:
                for root, _, fns in os.walk(f):
                    for fn in fns:
                        fp = os.path.join(root, fn)
                        an = fp[2:] if fp.startswith('./') else fp
                        zf.write(fp, an)
PYEOF
chmod +x "$_jdk_tools_dir/zip"

export PATH="$_jdk_tools_dir:$PATH"
