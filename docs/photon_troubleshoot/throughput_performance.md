# Throughput Performance

Throughtput performance over TCP might be reduced.

This might occur because timestamps are enabled by default and the parameter `net.ipv4.tcp_timestamps` has a value of 1.

Setting a value of 1 or 2 for this parameter may impact performance. Setting a value of 0 or 2 for this parameter might cause a security vulnerability. 