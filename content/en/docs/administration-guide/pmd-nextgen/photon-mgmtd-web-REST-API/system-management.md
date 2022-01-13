---
title:  System Management
weight: 2
---

## GET Method ##


### System Information ###

To fetch the complete system information, execute a GET request in the following format:

	curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock --request GET http://localhost/api/v1/system/describe

Example:

	curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock --request GET http://localhost/api/v1/system/describe | jq	% Total % Received % Xferd Average Speed Time Time Time Current	Dload Upload Total Spent Left Speed	100 5588 0 5588 0 0 42133 0 --:--:-- --:--:-- --:--:-- 42015



### CPU Information ###

To fetch information related to CPU, execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/cpuinfo

Example:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/cpuinfo


### Disk Usage Details ###


To fetch the usage details of the disk, execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/diskusage


Example:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/diskusage

**Response:**  
	
	{
	   "success":true,
	   "message":{
	      "path":"/",
	      "fstype":"ext2/ext3",
	      "total":269474643968,
	      "free":241944858624,
	      "used":13769904128,
	      "usedPercent":5.3848686637440935,
	      "inodesTotal":16777216,
	      "inodesUsed":101362,
	      "inodesFree":16675854,
	      "inodesUsedPercent":0.6041646003723145
	   },
	   "errors":""
	}


### Platform & kernel version details ###

To fetch the details about the platform and kernel versions on which the system is installed.

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/version

Example:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/version

**Response:**  
    
	{
	   "success":true,
	   "message":{
	      "hostname":"photon-4",
	      "uptime":10168492,
	      "bootTime":1627041016,
	      "procs":475,
	      "os":"linux",
	      "platform":"photon",
	      "platformFamily":"",
	      "platformVersion":"4.0",
	      "kernelVersion":"5.10.46-2.ph4",
	      "kernelArch":"x86_64",
	      "virtualizationSystem":"",
	      "virtualizationRole":"",
	      "hostId":"25a54d56-2249-524d-1355-e97b24e3415a"
	   },
	   "errors":""
	}


### Miscellaneous Hardware Details ###


To fetch miscellaneous harware details, execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/misc


Example:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/misc

**Response:**  

	{
	   "success":true,
	   "message":{
	      "175":"agpgart",
	      "183":"hw_random",
	      "228":"hpet",
	      "229":"fuse",
	      "231":"snapshot",
	      "235":"autofs",
	      "237":"loop-control",
	      "60":"vsock",
	      "61":"vmci",
	      "62":"cpu_dma_latency",
	      "63":"vga_arbiter"
	   },
	   "errors":""
	}


### User Details ###


To fetch the user details, execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/userstat

Example:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/userstat


### Virtual Memory Details ###


To fetch the details of the virtual memory, execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/virtualmemory

Example:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/virtualmemory

**Response:**  
    
	{
	   "success":true,
	   "message":{
	      "total":16810287104,
	      "available":15859195904,
	      "used":519139328,
	      "usedPercent":3.0882240427438687,
	      "free":9925554176,
	      "active":4017090560,
	      "inactive":2234974208,
	      "wired":0,
	      "laundry":0,
	      "buffers":171372544,
	      "cached":6194221056,
	      "writeBack":0,
	      "dirty":0,
	      "writeBackTmp":0,
	      "shared":9539584,
	      "slab":440422400,
	      "sreclaimable":370315264,
	      "sunreclaim":70107136,
	      "pageTables":6144000,
	      "swapCached":0,
	      "commitLimit":8405143552,
	      "committedAS":1310273536,
	      "highTotal":0,
	      "highFree":0,
	      "lowTotal":0,
	      "lowFree":0,
	      "swapTotal":0,
	      "swapFree":0,
	      "mapped":126369792,
	      "vmallocTotal":35184372087808,
	      "vmallocUsed":46546944,
	      "vmallocChunk":0,
	      "hugePagesTotal":0,
	      "hugePagesFree":0,
	      "hugePageSize":2097152
	   },
	   "errors":""
	}



### Kernel Module Details ###


To fetch the details about the kernel module, execute a GET request in the following format: 

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/modules


Example: 

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/modules


### Network ARP Details ###

To fetch the network ARP details, execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/net/arp


Example:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/net/arp

**Response:**  
    
	{
	   "success":true,
	   "message":[
	      {
	         "IPAddress":"",
	         "HWType":"",
	         "Flags":"",
	         "HWAddress":"",
	         "Mask":"",
	         "Device":""
	      },
	      {
	         "IPAddress":"10.197.103.253",
	         "HWType":"0x1",
	         "Flags":"0x2",
	         "HWAddress":"00:00:0c:9f:f4:28",
	         "Mask":"*",
	         "Device":"eth0"
	      },
	      {
	         "IPAddress":"10.197.103.162",
	         "HWType":"0x1",
	         "Flags":"0x2",
	         "HWAddress":"00:0c:29:b1:e6:16",
	         "Mask":"*",
	         "Device":"eth0"
	      },
	      {
	         "IPAddress":"10.197.103.251",
	         "HWType":"0x1",
	         "Flags":"0x2",
	         "HWAddress":"00:35:1a:9d:b8:e3",
	         "Mask":"*",
	         "Device":"eth0"
	      },
	      {
	         "IPAddress":"10.197.103.174",
	         "HWType":"0x1",
	         "Flags":"0x2",
	         "HWAddress":"00:0c:29:d3:c7:00",
	         "Mask":"*",
	         "Device":"eth0"
	      },
	      {
	         "IPAddress":"10.197.103.252",
	         "HWType":"0x1",
	         "Flags":"0x2",
	         "HWAddress":"00:f2:8b:e1:b0:13",
	         "Mask":"*",
	         "Device":"eth0"
	      },
	      {
	         "IPAddress":"10.197.103.91",
	         "HWType":"0x1",
	         "Flags":"0x2",
	         "HWAddress":"00:0c:29:41:07:8b",
	         "Mask":"*",
	         "Device":"eth0"
	      }
	   ],
	   "errors":""
	}



### Partition Details ###

To fetch the partition details, execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/partitions


Example:

	curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/partitions


### Platform Details ###

To fetch the details of the platform on which the system is installed, execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/platform


Example:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/platform

**Respose:**  
	
	{
	   "success":true,
	   "message":{
	      "Platform":"photon",
	      "Family":"",
	      "Version":"4.0"
	   },
	   "errors":""
	} 


### Swap Memory Details ###


To fetch the swap memory details, execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/swapmemory


Example:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/swapmemory

**Response:**  
    
	{
	   "success":true,
	   "message":{
	      "total":0,
	      "used":0,
	      "free":0,
	      "usedPercent":0,
	      "sin":0,
	      "sout":0,
	      "pgIn":0,
	      "pgOut":0,
	      "pgFault":0,
	      "pgMajFault":0
	   },
	   "errors":""
	}


### Input/Output Details of all Disk Partitions ###

To fetch the input/output (read/write) details of all the disk partition, execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/iocounters

Example:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock http://localhost/api/v1/proc/iocounters

**Response:**  

	{
	   "success":true,
	   "message":{
	      "loop0":{
	         "readCount":16407,
	         "mergedReadCount":0,
	         "writeCount":0,
	         "mergedWriteCount":0,
	         "readBytes":3999833088,
	         "writeBytes":0,
	         "readTime":6294,
	         "writeTime":0,
	         "iopsInProgress":0,
	         "ioTime":9088,
	         "weightedIO":6294,
	         "name":"loop0",
	         "serialNumber":"",
	         "label":""
	      },
	      "sda":{
	         "readCount":85357,
	         "mergedReadCount":13672,
	         "writeCount":212568,
	         "mergedWriteCount":783168,
	         "readBytes":5029398016,
	         "writeBytes":44981511680,
	         "readTime":54628,
	         "writeTime":17939082,
	         "iopsInProgress":0,
	         "ioTime":301572,
	         "weightedIO":17993710,
	         "name":"sda",
	         "serialNumber":"",
	         "label":""
	      },
	      "sda1":{
	         "readCount":351,
	         "mergedReadCount":0,
	         "writeCount":0,
	         "mergedWriteCount":0,
	         "readBytes":1437696,
	         "writeBytes":0,
	         "readTime":33,
	         "writeTime":0,
	         "iopsInProgress":0,
	         "ioTime":152,
	         "weightedIO":33,
	         "name":"sda1",
	         "serialNumber":"",
	         "label":""
	      },
	      "sda2":{
	         "readCount":128,
	         "mergedReadCount":23,
	         "writeCount":1,
	         "mergedWriteCount":0,
	         "readBytes":916480,
	         "writeBytes":512,
	         "readTime":38,
	         "writeTime":0,
	         "iopsInProgress":0,
	         "ioTime":56,
	         "weightedIO":38,
	         "name":"sda2",
	         "serialNumber":"",
	         "label":""
	      },
	      "sda3":{
	         "readCount":84806,
	         "mergedReadCount":13649,
	         "writeCount":212567,
	         "mergedWriteCount":783168,
	         "readBytes":5025352192,
	         "writeBytes":44981511168,
	         "readTime":54540,
	         "writeTime":17939082,
	         "iopsInProgress":0,
	         "ioTime":301444,
	         "weightedIO":17993623,
	         "name":"sda3",
	         "serialNumber":"",
	         "label":""
	      },
	      "sr0":{
	         "readCount":7,
	         "mergedReadCount":0,
	         "writeCount":0,
	         "mergedWriteCount":0,
	         "readBytes":1024,
	         "writeBytes":0,
	         "readTime":0,
	         "writeTime":0,
	         "iopsInProgress":0,
	         "ioTime":12,
	         "weightedIO":0,
	         "name":"sr0",
	         "serialNumber":"",
	         "label":""
	      }
	   },
	   "errors":""
	}

