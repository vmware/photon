---
title:  Configuring Photon Real-Time Operating System for Real-Time Applications
weight: 6 
---

Photon Real-Time (RT) Operating System (OS) (and the Linux kernel `PREEMPT_RT` patchset that it is based on) is optimized to support low-latency real-time scheduling and minimize the OS jitter as observed by real-time applications. However, to get the most out of Photon RT OS, it is must to have a proper system configuration. To run low-latency real time applications effectively, the sources of jitter have to be identified and eliminated across all layers of the underlying system, spanning the BIOS / firmware, the hypervisor, and the guest operating system (Photon RT).

## BIOS/Firmware ##
Tuning a system for real time operation starts from the lowest layers of the software stack, namely the System BIOS or Platform Firmware. The goal is to configure the settings for the following functions:

- Maximize Performance
Ex: Set CPU, memory and device power management modes to maximum performance, disable CPU idle states

- Minimize Computational Jitter
Ex: Disable Turbo Boost, disable Hyper-Threading

- Minimize System Management Interrupts
Ex: Disable options such as Processor Power and Utilization Monitoring, memory Pre-Failure Notification, and so on

Platform vendors often publish low-latency tuning guides for their BIOS/firmware. Refer documentation to learn about the recommended low-latency settings specific to your platform.

## Deploying Real-Time Applications on Photon Real-Time Operating System ##

A general strategy to deploy real-time applications on Photon RT is described as follows:


- Partition CPUs between the OS and the RT workload:
Among the available CPUs in the system, isolate a subset of CPUs, designated to run the RT workload. By default, the Linux scheduler will only run tasks on non-isolated CPUs, leaving the isolated CPUs to those tasks that are explicitly bound to them. Thus, all the housekeeping tasks of the OS will execute on non-isolated CPUs (with a few exceptions, such as per-CPU kernel threads). Then bind the RT workload to the isolated CPUs.

- Steer unrelated interrupts away from the CPUs running the RT workload:
Linux supports the ability to affine most interrupts to specific CPUs in the system. By using this mechanism, interrupts that are not relevant to the real-time workload can be affined to non-isolated CPUs, thus avoiding the jitter caused by interrupt handling latency on the isolated CPUs.

This strategy provides two important benefits:

1. It limits OS interference with the RT workload.

1. It protects the OS services from getting starved by the CPU-intensive RT tasks.

This configuration can be achieved using a combination of kernel command-line options, and user space packages, as discussed in the following sections.

### Kernel Command-Line Parameters ###



- CPU isolation

   `isolcpus=X,Y-Z (Ex: isolcpus=2,4-5)`


- Interrupt affinity

  `irqaffinity=X,Y-Z (Ex: irqaffinity=0-1,3)`  [ Usually it is the inverse of `isolcpus`.]


- RCU callbacks

 `rcu_nocbs=X,Y-Z` [ Usually it is same as `isolcpus`. ]
 `rcu_nocb_poll=1`


- NOHZ (Eliminating the periodic timer)

    `nohz=on`
    `nohz_full=X,Y-Z` [ Usually it is same as `isolcpus`. ]


- CPU idle

    `idle=halt or idle=poll`
    `intel_idle.max_cstate=0 cpuidle.off=1`


- CPU frequency

    `intel_pstate=disable`


- Lockup detectors

    `nosoftlockup nowatchdog nmi_watchdog=0`


- Timer skew detection

        skew_tick=1
        clocksource=tsc
        tsc=reliable

The full list of kernel command-line parameters and their descriptions are available at [https://www.kernel.org/doc/html/v5.10/admin-guide/kernel-parameters.html](https://www.kernel.org/doc/html/v5.10/admin-guide/kernel-parameters.html)


### Tuned configuration ###
Tuned is a system tuning daemon that offers several profiles to tailor the OS to various usecases, including a 'realtime' profile for low-latency workloads.

The realtime tuned profile can be applied as shown below:
    
    

- `	tdnf install tuned`
    

- `systemctl enable tuned`
    

- `systemctl start tuned`

 Add `isolcpus` to `/etc/tuned/realtime-variables.conf` (by uncommenting the isolated_cores= parameter):

   ` $ cat /etc/tuned/realtime-variables.conf`

    Examples:
   ` # isolated_cores=2,4-7`

Note: The cores configured as isolated in tuned should be consistent with isolcpus in the kernel command-line.

    tuned-adm profile realtime

### Stalld configuration ###
The stalld daemon monitors the system for starved tasks and revives them by giving them a temporary boost using the `SCHED_DEADLINE` policy. `stalld` offers fine-grained controls to give starved tasks a user-specified amount of CPU time.

The stalld configuration file is `/etc/sysconfig/stalld`.

The key parameters are Starving Threshold (THRESH), Boost Period (BP), Boost Runtime (BR), and Boost Duration (BD).

The mode of operation is as follows: 

If a task is starved for at least `THRESH` seconds, it is scheduled using `SCHED_DEADLINE` scheduling policy, so that it will run at least `BR` nanoseconds in every `BP` nanoseconds time period, and this repeats up to `BD` seconds, after which the task gets back its original scheduler policy/priority settings.


### Real Time Scheduling Policies ###

The Linux kernel offers several scheduling policies to support various applications, among which the real time policies are highlighted below:



- SCHED_OTHER (default policy), SCHED_BATCH, SCHED_IDLE (non real-time policies)

- SCHED_FIFO (First-In First-Out Real Time Scheduling)



1. Priority Range: 1 to 99 (highest)


1. Algorithm: The scheduler runs the highest-priority runnable task in the SCHED_FIFO scheduling class, until it yields (blocks/waits) the CPU voluntarily.



- SCHED_RR (Round-Robin Real Time Scheduling)



1. Priority Range: 1 to 99 (highest)


1. Algorithm: The scheduler runs the highest-priority SCHED_RR task, and time-slices between equal-priority SCHED_RR tasks in configurable intervals. 



- SCHED_DEADLINE ( Earliest Deadline First Real Time Scheduling)


1. Key parameters: Runtime, Period and Deadline, which can be configured on a per-task basis.


1. Algorithm: The scheduler gives a SCHED_DEADLINE task at least `Runtime` amount of time on the CPU in every `Period` time period, before `Deadline` time is up.

### Real Time Throttling ###

The Linux kernel offers proc file system (procfs) controls to influence real-time task scheduling and throttling.

The RT throttling algorithm is as follows:

- All real-time tasks are throttled to run up to `runtime` microseconds, in every `period` microseconds. The remaining time in `period` microseconds is used to run non-RT tasks in the system.



- `runtime` and `period` values can be configured by writing to the files listed as follows:

    
1. `/proc/sys/kernel/sched_rt_runtime_us`
    Default: 95% (950000)
    Range: -1 to (INT_MAX -1)  [ -1 implies no limit, i.e., no throttling ]
    
   
1.  `/proc/sys/kernel/sched_rt_period_us`
    Default: 1s (1000000)
    Range: 1 to INT_MAX


Note: See Command Line Reference for the commands for manipulating real-time properties of processes.