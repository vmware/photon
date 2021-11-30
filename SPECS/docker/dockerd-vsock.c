/*
 * Docker daemon vsock listener launcher
 *
 * Copyright (C) 2021 VMware, Inc. All Rights Reserved.
 */

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <stdlib.h>
#include <stdio.h>
#include <err.h>
#include <error.h>
#include <unistd.h>
#include <sys/socket.h>
#include <linux/vm_sockets.h>

#define SOCK_NAME "vsock.sock"
#define SOCK_DEFAULT_PORT 1024
#define DOCKERD_ARG0 "dockerd"
#define DOCKERD_PATH "/usr/bin/dockerd"

__attribute__((noreturn)) void run(char **argv) {
   argv[0] = DOCKERD_ARG0;
   if (execv(DOCKERD_PATH, argv) == -1) {
      err(1, "exec failed");
   }
   __builtin_unreachable();
}

int main(int argc, char **argv) {
   struct sockaddr_vm vsockAddr = { AF_VSOCK };

   vsockAddr.svm_cid = VMADDR_CID_ANY;

   const char *vsockPort = getenv("VSOCK_PORT");
   if (vsockPort) {
      vsockAddr.svm_port = atoi(vsockPort);
   }
   if (!vsockAddr.svm_port) {
      vsockAddr.svm_port = SOCK_DEFAULT_PORT;
   }

   int sockfd = socket(AF_VSOCK, SOCK_STREAM, 0);
   if (sockfd == -1) {
      err(1, "socket failed");
   }

   if (bind(sockfd, (struct sockaddr *)&vsockAddr, sizeof vsockAddr) != 0) {
      err(1, "bind failed");
   }
   if (listen(sockfd, 1) != 0 ) {
      err(1, "listen failed");
   }

   char *newListens = NULL, *newListenNames = NULL;

   const char *sdListens = getenv("LISTEN_FDS");
   const char *sdListenNames = getenv("LISTEN_FDNAMES");
   if (!sdListens ^ !sdListenNames) {
       error(1, 0, "both LISTEN_FDS and LISTEN_FDNAMES "
                   "must be present, or neither");
   }
   int nextListen = 3;
   if (sdListens) {
      nextListen += atoi(sdListens);
   }
   if (sockfd != nextListen) {
      error(1, 0, "sockfd must be adjacent to LISTEN_FDS");
   }
   if (asprintf(&newListens, "%d", sockfd - 2) == -1 ||
       asprintf(&newListenNames, "%s%s%s",
                sdListens ? sdListenNames : "",
                sdListens ? ":" : "",
                SOCK_NAME) == -1) {
      abort();
   }
   setenv("LISTEN_FDS", newListens, 1);
   setenv("LISTEN_FDNAMES", newListenNames, 1);
   free(newListenNames);
   free(newListens);
   run(argv);
   return 0;
}
