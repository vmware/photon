# System-wide GDB initialization file.
python
import glob
# glob.iglob is not available in python-2.4 (RHEL-5).
for f in glob.glob('/etc/gdbinit.d/*.gdb'):
  gdb.execute('source %s' % f)
for f in glob.glob('/etc/gdbinit.d/*.py'):
  gdb.execute('source %s' % f)
end
