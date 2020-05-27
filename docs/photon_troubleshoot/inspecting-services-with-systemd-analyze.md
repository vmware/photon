# Inspecting Services with `systemd-analyze`

The `systemd-analyze` command reveals performance statistics for boot times, traces system services, and verifies unit files. It can help troubleshoot slow system boots and incorrect unit files. See the man page for a list of options. 

Examples:

	systemd-analyze blame

	systemd-analyze dump