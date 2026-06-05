#!/bin/bash
# zip and unzip are deprecated in Photon 5.0+.
# This script creates lightweight Python-based wrappers for both tools and
# prepends their directory to PATH so that build scripts can locate them.

_jdk_tools_dir="/usr/bin"
#$(mktemp -d /tmp/jdk-tools.XXXXXX)

cat > "$_jdk_tools_dir/unzip" << 'PYEOF'
#!/usr/bin/env python3

import os
import shutil
import sys
import zipfile

args = sys.argv[1:]

extract = True
list_only = False
stdout_mode = False
junk_paths = False

overwrite = True
outdir = '.'
zippath = None
members = []
exclude = []

expanded = []
for arg in args:
  if arg.startswith('-') and not arg.startswith('--') and len(arg) > 2:
    for ch in arg[1:]:
      expanded.append('-' + ch)
  else:
    expanded.append(arg)

args = expanded

i = 0
while i < len(args):
  arg = args[i]

  if arg == '-q':
    i += 1

  elif arg == '-o':
    overwrite = True
    i += 1

  elif arg == '-n':
    overwrite = False
    i += 1

  elif arg == '-u':
    overwrite = True
    i += 1

  elif arg == '-j':
    junk_paths = True
    i += 1

  elif arg == '-a':
    i += 1

  elif arg == '-l':
    list_only = True
    extract = False
    i += 1

  elif arg == '-v':
    list_only = True
    extract = False
    i += 1

  elif arg == '-p':
    stdout_mode = True
    extract = False
    i += 1

  elif arg == '-d' and i + 1 < len(args):
    outdir = args[i + 1]
    i += 2

  elif arg == '-x':
    i += 1
    while i < len(args) and not args[i].startswith('-'):
      exclude.append(args[i])
      i += 1

  elif arg.startswith('-'):
    i += 1

  else:
    if zippath is None:
      zippath = arg
    else:
      members.append(arg)
    i += 1

if zippath is None:
  sys.exit(1)

if not os.path.exists(zippath) and not zippath.endswith('.zip'):
  alt = zippath + '.zip'
  if os.path.exists(alt):
    zippath = alt

with zipfile.ZipFile(zippath) as zf:

  names = zf.namelist()

  if members:
    selected = []
    for n in names:
      if n in members:
        selected.append(n)
  else:
    selected = names

  if exclude:
    filtered = []
    for n in selected:
      skip = False
      for pat in exclude:
        if shutil.fnmatch.fnmatch(n, pat):
          skip = True
          break
      if not skip:
        filtered.append(n)
    selected = filtered

  if list_only:
    for n in selected:
      info = zf.getinfo(n)
      print(f'{info.file_size:>9}  {n}')
    sys.exit(0)

  if stdout_mode:
    for n in selected:
      if n.endswith('/'):
        continue
      sys.stdout.buffer.write(zf.read(n))
    sys.exit(0)

  os.makedirs(outdir, exist_ok=True)

  for n in selected:
    if n.endswith('/'):
      continue

    target = os.path.basename(n) if junk_paths else n
    dest = os.path.join(outdir, target)

    os.makedirs(os.path.dirname(dest) or '.', exist_ok=True)

    if not overwrite and os.path.exists(dest):
      continue

    with zf.open(n) as src, open(dest, 'wb') as dst:
      shutil.copyfileobj(src, dst)

    info = zf.getinfo(n)
    mode = (info.external_attr >> 16) & 0o777
    if mode:
      try:
        os.chmod(dest, mode)
      except OSError:
        pass
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
