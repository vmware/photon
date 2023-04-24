---
title:  Photon Real-Time Operating System Command-line Interface
weight: 4
---

Photon Real-Time Operating System provides commands for manipulating real-time properties of processes.

## tuna

The tuna utility can be used to view and modify process priorities, CPU isolation and other real time characteristics in the system.

Examples:

View processes and their RT scheduling policies and priorities:
    $ tuna -P

                     thread    ctxt_switches

    pid   SCHED_rtpri  affinity   voluntary    nonvoluntary                    cmd

      1    OTHER    0         0       1211           917                     systemd 

      2    OTHER     0        0       281             0                      kthreadd 

      3    OTHER     0        0         3             1                         rcu_gp
 
      4    OTHER     0        0         2             1                    rcu_par_gp
 
      6    OTHER     0        0         8             1            kworker/0:0H-kblockd

     13    FIFO      1        0       317             1                     rcu_sched

     16    FIFO     99        0         3             2                posixcputmr/0 

     17    FIFO     99        0         6             2                    migration/0

    679    FIFO     50        0     1647541           1                irq/58-eth0-rxt


The following tasks are performed by using the `tuna` command:

- Isolate a set of CPUs

    `$ tuna -c <cpulist> -i  (where <cpulist> can be X,Y-Z)`


- See the list of processes running on the specific CPUs before and after isolation
    
        $ tuna -c <cpulist> --show_threads
        $ tuna -c <cpulist> -i --show_threads


## taskset

The taskset command can be used to get/set CPU affinity of tasks:

- Run a program bound to a set of CPUs

    `$ taskset -c <cpulist> ./program (where <cpulist> can be X,Y-Z)`

- Move a running task to a set of CPUs
    `$ taskset -c p <cpulist> <pid>`

- View the CPU affinity settings of a running task
     ` $ taskset -c -p <pid>`
    

  


## chrt

The `chrt` command can be used to get or set the real-time scheduling policies and priorities of processes:

- Modify the scheduling policy and priority of a running task
 
 ` $ chrt -f -p <priority> <pid>`  (sets the task with pid <pid> to SCHED_FIFO policy with priority <priority>)


- View the current scheduling policy and priority of a running task

   ` $ chrt -p <pid>`



## ps

The `ps` command can be used to list processes with their scheduling policies and priorities:


    $ ps -eo cmd,pid,cpu,pri,cls


     `CMD `                                              ` PID  CPU   PRI    CLS`

    `/lib/systemd/systemd --swit `                       ` 1     -    19    TS`

    `[kthreadd]`                                         ` 2     -    19    TS`
