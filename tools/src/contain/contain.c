#define _GNU_SOURCE
#include <errno.h>
#include <error.h>
#include <fcntl.h>
#include <grp.h>
#include <sched.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sysexits.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include "contain.h"

void usage(char *progname) {
  fprintf(stderr, "\
Usage: %s [OPTIONS] DIR [CMD [ARG]...]\n\
Options:\n\
  -b BND    bind host path into container\n\
  -c        deactivate console emulation in the container\n\
  -g MAP    set the container-to-host GID map\n\
  -i CMD    run a helper child inside the new namespaces\n\
  -n        share the host network unprivileged in the container\n\
  -o CMD    run a helper child outside the new namespaces\n\
  -u MAP    set the container-to-host UID map\n\
BND is specified as HOST_DIR:CONTAINER_DIR[,HOST_DIR2:CONTAINER_DIR2]...\n\
GID and UID maps are specified as START:LOWER:COUNT[,START:LOWER:COUNT]...\n\
", progname);
  exit(EX_USAGE);
}

int main(int argc, char **argv) {
  char *gidmap = NULL, *inside = NULL, *outside = NULL, *uidmap = NULL;
  char *bind = NULL;
  int hostnet = 0, primary, option, stdio = 0;
  pid_t child, parent;

  while ((option = getopt(argc, argv, "+:b:cg:i:no:u:")) > 0)
    switch (option) {
      case 'b':
        bind = optarg;
        break;
      case 'c':
        stdio++;
        break;
      case 'g':
        gidmap = optarg;
        break;
      case 'i':
        inside = optarg;
        break;
      case 'n':
        hostnet++;
        break;
      case 'o':
        outside = optarg;
        break;
      case 'u':
        uidmap = optarg;
        break;
      default:
        usage(argv[0]);
    }

  if (argc <= optind)
    usage(argv[0]);

  parent = getpid();
  switch (child = fork()) {
    case -1:
      error(1, errno, "fork");
      break;
    case 0:
      raise(SIGSTOP);
      if (geteuid() != 0)
        denysetgroups(parent);
      writemap(parent, GID, gidmap);
      writemap(parent, UID, uidmap);

      if (outside) {
        if (setgid(getgid()) < 0 || setuid(getuid()) < 0)
          error(1, 0, "Failed to drop privileges");
        execlp(SHELL, SHELL, "-c", outside, NULL);
        error(1, errno, "exec %s", outside);
      }

      exit(EXIT_SUCCESS);
  }

  if (setgid(getgid()) < 0 || setuid(getuid()) < 0)
    error(1, 0, "Failed to drop privileges");

  if (unshare(CLONE_NEWIPC | CLONE_NEWNS | CLONE_NEWUSER | CLONE_NEWUTS) < 0)
    error(1, 0, "Failed to unshare namespaces");

  if (!hostnet && unshare(CLONE_NEWNET) < 0)
      error(1, 0, "Failed to unshare network namespace");

  waitforstop(child);
  kill(child, SIGCONT);
  waitforexit(child);

  if (setgid(0)) {
      error(1, errno, "setgid");
  }

  if (setgroups(0, NULL)) {
      error(1, errno, "setgroups");
  }

  if (setuid(0)) {
      error(1, errno, "setuid");
  }

  primary = stdio ? -1 : getconsole();
  createroot(argv[optind], primary, inside, bind);

  unshare(CLONE_NEWPID);
  switch (child = fork()) {
    case -1:
      error(1, errno, "fork");
      break;
    case 0:
      mountproc();
      if (!hostnet)
        mountsys();
      enterroot();

      if (primary >= 0) {
        close(primary);
        setconsole("/dev/console");
      }

      clearenv();
      putenv("container=contain");

      if (argv[optind + 1])
        execv(argv[optind + 1], argv + optind + 1);
      else
        execl(SHELL, SHELL, NULL);
      error(1, errno, "exec");
  }

  return supervise(child, primary);
}
