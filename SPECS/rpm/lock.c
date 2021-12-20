/*
 * Helper program to lock a file
 *
 * Using this in rpm-rebuilddb.sh to lock rpm directory
 * This will help to manage contention between rpm transactions & rebuilddb
 * operation.
 */

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>
#include <stdint.h>
#include <stdbool.h>

/*
 * This file acts as a flag to indicate that lock is obtained
 */
#define LOCK_FLAG "/var/run/.lkflg"

static bool volatile sigint = false;

static int32_t lock_fd = 0;

static struct flock fl = {F_WRLCK, SEEK_SET, 0, 0, 0};

void handle_sigint(int32_t sig)
{
    sigint = true;
    fl.l_type = F_UNLCK;
    if (fcntl(lock_fd, F_SETLK, &fl) < 0) {
        perror("fcntl unlock\n");
        exit(EXIT_FAILURE);
    }

    close(lock_fd);
    lock_fd = -1;
    unlink(LOCK_FLAG);
    exit(EXIT_SUCCESS);
}

int32_t main(int32_t argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <file path>\n", argv[0]);
        return -1;
    }

    lock_fd = open(argv[1], O_CREAT|O_RDWR);
    if (lock_fd < 0) {
        perror("open lock file\n");
        return -1;
    }

    signal(SIGINT, handle_sigint);

    fl.l_pid = 0;
    printf("Trying to get lock on %s(pid: %d) ...\n", argv[1], getpid());
    fflush(stdout);
    if (fcntl(lock_fd, F_SETLKW, &fl) == -1) {
        perror("fcntl lock\n");
        return -1;
    }

    {
        int32_t lockflg_fd = 0;
        lockflg_fd = open(LOCK_FLAG, O_CREAT|O_RDWR);
        if (lockflg_fd < 0) {
            perror("open lock flag\n");
            return -1;
        }
        close(lockflg_fd);
    }
    printf("Got lock(pid: %d)\n", getpid());
    fflush(stdout);

    while (!sigint) {
        sleep(1);
    }

    if (lock_fd >= 0) {
        handle_sigint(0);
    }

    return 0;
}
