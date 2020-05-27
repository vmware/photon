# Performance Issues

Performance issues can be difficult to troubleshoot because so many variables play a role in overall system performance. Interpreting performance data often depends on the context and the situation. To better identify and isolate variables and to gain insight into performance data, you can use the troubleshooting tools on Photon OS to diagnose the system.  

If you have no indication what the cause of a performance degradation might be, start by getting a high-level picture of the system's state. Then look for signs in the data that might point to a cause. 

Use the following guidelines to gain insight into performance data:

- Start with the `systemd journal`.

- The `top` tool can unmask problems caused by processes or applications overconsuming CPUs, time, or RAM. If the percent of CPU utilization is consistently high with little idle time, for example, there might be a runaway process. Restart it.

- The `netstat --statistics` command can identify bottlenecks causing performance issues. It lists interface statistics for different protocols.

- If `top` and `netstat` reveal no errors, run the `strace ls -al` to view every system call.

- The `watch` command can help dynamically monitor a command to help troubleshoot performance issues:

    `watch -n0 --differences <command>`
    
    You can also combine `watch` with the `vmstat` command to dig deeper into statistics about virtual memory, processes, block input-output, disks, and CPU activity. Are there any bottlenecks?

- You can use the `dstat` utility to see the live, running list of statistics about system resources.

- The `systemd-analyze` reveals performance statistics for boot time and can help troubleshoot slow system boots and incorrect unit files.

The additional tools that you select depend on the clues that your initial investigation reveals. The following tools can also help troubleshoot performance: `sysstat`, `sar`, `systemtap`, and `crash`. 

