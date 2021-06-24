#define _GNU_SOURCE
#include <errno.h>
#include <error.h>
#include <fcntl.h>
#include <limits.h>
#include <poll.h>
#include <signal.h>
#include <stdlib.h>
#include <termios.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/signalfd.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <sys/wait.h>
#include "contain.h"

static struct termios saved;

int getconsole(void) {
  int primary;

  if ((primary = posix_openpt(O_RDWR | O_NOCTTY)) < 0)
    error(1, 0, "Failed to allocate a console pseudo-terminal");
  grantpt(primary);
  unlockpt(primary);
  return primary;
}

static void rawmode() {
  struct termios termios;

  if (!isatty(STDIN_FILENO))
    return;
  if (tcgetattr(STDIN_FILENO, &termios) < 0)
    error(1, errno, "tcgetattr");
  cfmakeraw(&termios);
  tcsetattr(STDIN_FILENO, TCSANOW, &termios);
}

static void restoremode() {
  if (isatty(STDIN_FILENO))
    tcsetattr(STDIN_FILENO, TCSANOW, &saved);
}

static void savemode() {
  if (isatty(STDIN_FILENO) && tcgetattr(STDIN_FILENO, &saved) < 0)
    error(1, errno, "tcgetattr");
}

void setconsole(char *name) {
  int console;
  struct termios termios;

  setsid();

  if ((console = open(name, O_RDWR)) < 0)
    error(1, 0, "Failed to open console in container");
  ioctl(console, TIOCSCTTY, NULL);

  if (tcgetattr(console, &termios) < 0)
    error(1, errno, "tcgetattr");
  termios.c_iflag |= IGNBRK | IUTF8;
  tcsetattr(console, TCSANOW, &termios);

  dup2(console, STDIN_FILENO);
  dup2(console, STDOUT_FILENO);
  dup2(console, STDERR_FILENO);
  if (console != STDIN_FILENO)
    if (console != STDOUT_FILENO)
      if (console != STDERR_FILENO)
        close(console);
}

int supervise(pid_t child, int console) {
  char buffer[PIPE_BUF];
  int signals, status;
  sigset_t mask;
  ssize_t count, length, offset;
  struct pollfd fds[3];

  if (console < 0) {
    if (waitpid(child, &status, 0) < 0)
      error(1, errno, "waitpid");
    return WIFEXITED(status) ? WEXITSTATUS(status) : EXIT_FAILURE;
  }

  sigemptyset(&mask);
  sigaddset(&mask, SIGCHLD);
  sigprocmask(SIG_BLOCK, &mask, NULL);
  if ((signals = signalfd(-1, &mask, 0)) < 0)
    error(1, errno, "signalfd");

  if (waitpid(child, &status, WNOHANG) > 0)
    if (WIFEXITED(status) || WIFSIGNALED(status))
      raise(SIGCHLD);

  savemode();
  atexit(restoremode);
  rawmode();

  fds[0].fd = console;
  fds[0].events = POLLIN;
  fds[1].fd = STDIN_FILENO;
  fds[1].events = POLLIN;
  fds[2].fd = signals;
  fds[2].events = POLLIN;

  while (1) {
    if (poll(fds, 3, -1) < 0)
        if (errno != EAGAIN && errno != EINTR)
          error(1, errno, "poll");

    if (fds[0].revents & (POLLIN | POLLHUP)) {
      while ((length = read(console, buffer, sizeof(buffer))) < 0)
        if (errno != EAGAIN && errno != EINTR)
          error(1, errno, "read");
      if (length > 0) {
        for (offset = 0; length > 0; offset += count, length -= count)
          while ((count = write(STDOUT_FILENO, buffer + offset, length)) < 0)
            if (errno != EAGAIN && errno != EINTR)
              error(1, errno, "write");
      } else {
        fds[0].events = 0;
      }
    }

    if (fds[1].revents & (POLLIN | POLLHUP)) {
      while ((length = read(STDIN_FILENO, buffer, sizeof(buffer))) < 0)
        if (errno != EAGAIN && errno != EINTR)
          error(1, errno, "read");
      if (length > 0) {
        for (offset = 0; length > 0; offset += count, length -= count)
          while ((count = write(console, buffer + offset, length)) < 0)
            if (errno != EAGAIN && errno != EINTR)
              error(1, errno, "write");
      } else {
        fds[1].events = 0;
      }
    }

    if (fds[2].revents & POLLIN) {
      while (read(signals, buffer, sizeof(buffer)) < 0)
        if (errno != EAGAIN && errno != EINTR)
          error(1, errno, "read");
      if (waitpid(child, &status, WNOHANG) > 0)
        if (WIFEXITED(status) || WIFSIGNALED(status))
          break;
    }
  }

  close(signals);
  return WIFEXITED(status) ? WEXITSTATUS(status) : EXIT_FAILURE;
}
