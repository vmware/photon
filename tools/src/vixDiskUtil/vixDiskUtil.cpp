/* *************************************************
 * Copyright 2007-2015 VMware, Inc.
 * *************************************************/

/*
 * vixDiskUtil.cpp --
 *
 *      Helper program to create and mount vmdk files.
 */

#include <dlfcn.h>
#include <sys/time.h>

#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>
#include <stdexcept>

#include "vixDiskLib.h"
#include "vixMntapi.h"

using std::cout;
using std::string;
using std::endl;
using std::vector;

#define COMMAND_CREATE          (1 << 0)
#define COMMAND_DUMP            (1 << 1)
#define COMMAND_FILL            (1 << 2)
#define COMMAND_INFO            (1 << 3)
#define COMMAND_REDO            (1 << 4)
#define COMMAND_DUMP_META       (1 << 5)
#define COMMAND_READ_META       (1 << 6)
#define COMMAND_WRITE_META      (1 << 7)
#define COMMAND_MULTITHREAD     (1 << 8)
#define COMMAND_CLONE           (1 << 9)
#define COMMAND_READBENCH       (1 << 10)
#define COMMAND_WRITEBENCH      (1 << 11)
#define COMMAND_CHECKREPAIR     (1 << 12)
#define COMMAND_MOUNTDISK       (1 << 13)
#define COMMAND_CONVERT     (1 << 14)

#define VIXDISKLIB_VERSION_MAJOR 6
#define VIXDISKLIB_VERSION_MINOR 0
#define VIXMNTAPI_VERSION_MAJOR 1
#define VIXMNTAPI_VERSION_MINOR 0

// Default buffer size (in sectors) for read/write benchmarks
#define DEFAULT_BUFSIZE 128

// Print updated statistics for read/write benchmarks roughly every
// BUFS_PER_STAT sectors (current value is 64MBytes worth of data)
#define BUFS_PER_STAT (128 * 1024)
// Character array for random filename generation
static const char randChars[] = "0123456789"
   "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

// Per-thread information for multi-threaded VixDiskLib test.
struct ThreadData {
   std::string dstDisk;
   VixDiskLibHandle srcHandle;
   VixDiskLibHandle dstHandle;
   VixDiskLibSectorType numSectors;
};

static struct {
    int command;
    VixDiskLibAdapterType adapterType;
    VixDiskLibDiskType diskType;
    char *transportModes;
    char *diskPath;
    char *parentPath;
    char *metaKey;
    char *metaVal;
    int filler;
    unsigned mbSize;
    VixDiskLibSectorType numSectors;
    VixDiskLibSectorType startSector;
    VixDiskLibSectorType bufSize;
    uint32 openFlags;
    unsigned numThreads;
    Bool success;
    Bool isRemote;
    char *host;
    char *userName;
    char *password;
    char *thumbPrint;
    int port;
    char *srcPath;
    VixDiskLibConnection connection;
    char *vmxSpec;
    bool useInitEx;
    char *cfgFile;
    char *libdir;
    char *ssMoRef;
    int repair;
} appGlobals;

static int ParseArguments(int argc, char* argv[]);
static void DoCreate(void);
static void DoRedo(void);
static void DoFill(void);
static void DoDump(void);
static void DoMountDisk(void);
static void DoReadMetadata(void);
static void DoWriteMetadata(void);
static void DoDumpMetadata(void);
static void DoInfo(void);
static void DoTestMultiThread(void);
static void DoClone(void);
static void DoConvert(void);
static int BitCount(int number);
static void DumpBytes(const uint8 *buf, size_t n, int step);
static void DoRWBench(bool read);
static void DoCheckRepair(Bool repair);


#define THROW_ERROR(vixError) \
   throw VixDiskLibErrWrapper((vixError), __FILE__, __LINE__)

#define CHECK_AND_THROW(vixError)                                    \
   do {                                                              \
      if (VIX_FAILED((vixError))) {                                  \
         throw VixDiskLibErrWrapper((vixError), __FILE__, __LINE__); \
      }                                                              \
   } while (0)

/*
 *----------------------------------------------------------------------
 *
 * GenerateRandomFilename --
 *
 *      Generate and return a random filename.
 *
 * Results:
 *      None
 *
 * Side effects:
 *      None.
 *
 *----------------------------------------------------------------------
 */
static void
GenerateRandomFilename(const string& prefix, string& randomFilename)
{
    string retStr;
    int strLen = sizeof(randChars) - 1;

    for (unsigned int i = 0; i < 8; i++)
    {
        retStr += randChars[rand() % strLen];
    }
    randomFilename = prefix + retStr;
}


/*
 *--------------------------------------------------------------------------
 *
 * LogFunc --
 *
 *      Callback for VixDiskLib Log messages.
 *
 * Results:
 *      None.
 *
 * Side effects:
 *      None.
 *
 *--------------------------------------------------------------------------
 */

static void
LogFunc(const char *fmt, va_list args)
{
   printf("Log: ");
   vprintf(fmt, args);
}


/*
 *--------------------------------------------------------------------------
 *
 * WarnFunc --
 *
 *      Callback for VixDiskLib Warning messages.
 *
 * Results:
 *      None.
 *
 * Side effects:
 *      None.
 *
 *--------------------------------------------------------------------------
 */

static void
WarnFunc(const char *fmt, va_list args)
{
   printf("Warning: ");
   vprintf(fmt, args);
}


/*
 *--------------------------------------------------------------------------
 *
 * PanicFunc --
 *
 *      Callback for VixDiskLib Panic messages.
 *
 * Results:
 *      None.
 *
 * Side effects:
 *      None.
 *
 *--------------------------------------------------------------------------
 */

static void
PanicFunc(const char *fmt, va_list args)
{
   printf("Panic: ");
   vprintf(fmt, args);
   exit(10);
}

typedef void (VixDiskLibGenericLogFunc)(const char *fmt, va_list args);


// Wrapper class for VixDiskLib disk objects.

class VixDiskLibErrWrapper
{
public:
    explicit VixDiskLibErrWrapper(VixError errCode, const char* file, int line)
          :
          _errCode(errCode),
          _file(file),
          _line(line)
    {
        char* msg = VixDiskLib_GetErrorText(errCode, NULL);
        _desc = msg;
        VixDiskLib_FreeErrorText(msg);
    }

    VixDiskLibErrWrapper(const char* description, const char* file, int line)
          :
         _errCode(VIX_E_FAIL),
         _desc(description),
         _file(file),
         _line(line)
    {
    }

    string Description() const { return _desc; }
    VixError ErrorCode() const { return _errCode; }
    string File() const { return _file; }
    int Line() const { return _line; }

private:
    VixError _errCode;
    string _desc;
    string _file;
    int _line;
};

class VixDisk
{
public:

    VixDiskLibHandle Handle() { return _handle; }
    VixDisk(VixDiskLibConnection connection, char *path, uint32 flags)
    {
       _handle = NULL;
       VixError vixError = VixDiskLib_Open(connection, path, flags, &_handle);
       CHECK_AND_THROW(vixError);
       printf("Disk \"%s\" is open using transport mode \"%s\".\n",
              path, VixDiskLib_GetTransportMode(_handle));
    }

    ~VixDisk()
    {
        if (_handle) {
           VixDiskLib_Close(_handle);
        }
        _handle = NULL;
    }

private:
    VixDiskLibHandle _handle;
};


/*
 *--------------------------------------------------------------------------
 *
 * PrintUsage --
 *
 *      Displays the usage message.
 *
 * Results:
 *      1.
 *
 * Side effects:
 *      None.
 *
 *--------------------------------------------------------------------------
 */

static int
PrintUsage(void)
{
    printf("Usage: vixdiskutil command [options] diskPath\n\n");

    printf("List of commands (all commands are mutually exclusive):\n");
    printf(" -create : creates a sparse virtual disk with capacity "
           "specified by -cap\n");
    printf(" -redo parentPath : creates a redo log 'diskPath' "
           "for base disk 'parentPath'\n");
    printf(" -info : displays information for specified virtual disk\n");
    printf(" -dump : dumps the contents of specified range of sectors "
           "in hexadecimal\n");
    printf(" -fill : fills specified range of sectors with byte value "
           "specified by -val\n");
    printf(" -mount : mounts the disk on to local path\n");
    printf(" -wmeta key value : writes (key,value) entry into disk's metadata table\n");
    printf(" -rmeta key : displays the value of the specified metada entry\n");
    printf(" -meta : dumps all entries of the disk's metadata\n");
    printf(" -clone sourcePath : clone source vmdk possibly to a remote site\n");
    printf(" -convert sourcePath : convert source raw image to a vmdk\n");
    printf(" -readbench blocksize: Does a read benchmark on a disk using the \n");
    printf("specified I/O block size (in sectors).\n");
    printf(" -writebench blocksize: Does a write benchmark on a disk using the\n");
    printf("specified I/O block size (in sectors). WARNING: This will\n");
    printf("overwrite the contents of the disk specified.\n");
    printf(" -check repair: Check a sparse disk for internal consistency, "
           "where repair is a boolean value to indicate if a repair operation "
           "should be attempted.\n\n");

    printf("options:\n");
    printf(" -adapter [ide|scsi|lsilogic] : bus adapter type for 'create' option "
           "(default='scsi')\n");
    printf(" -disktype [1-6] : virtual disk type for 'create' option"
           "(default='VIXDISKLIB_DISK_MONOLITHIC_SPARSE')\n");
    printf("	1 - VIXDISKLIB_DISK_MONOLITHIC_SPARSE \n");
    printf("	2 - VIXDISKLIB_DISK_MONOLITHIC_FLAT \n");
    printf("	3 - VIXDISKLIB_DISK_SPLIT_SPARSE \n");
    printf("	4 - VIXDISKLIB_DISK_SPLIT_FLAT \n");
    printf("	5 - VIXDISKLIB_DISK_VMFS_FLAT \n");
    printf("	6 - VIXDISKLIB_DISK_STREAM_OPTIMIZED \n");
    printf(" -start n : start sector for 'dump/fill' options (default=0)\n");
    printf(" -count n : number of sectors for 'dump/fill' options (default=1)\n");
    printf(" -val byte : byte value to fill with for 'write' option (default=255)\n");
    printf(" -cap megabytes : capacity in MB for -create option (default=100)\n");
    printf(" -single : open file as single disk link (default=open entire chain)\n");
    printf(" -multithread n: start n threads and copy the file to n new files\n");
    printf(" -host hostname : hostname/IP address of VC/vSphere host (Mandatory)\n");
    printf(" -user userid : user name on host (Mandatory) \n");
    printf(" -password password : password on host. (Mandatory)\n");
    printf(" -port port : port to use to connect to host (default = 443) \n");
    printf(" -vm moref=id : id is the managed object reference of the VM \n");
    printf(" -libdir dir : Folder location of the VDDK installation. "
           "On Windows, the bin folder holds the plugin.  On Linux, it is "
           "the lib64 directory\n");
    printf(" -initex configfile : Specify path and filename of config file \n");
    printf(" -ssmoref moref : Managed object reference of VM snapshot \n");
    printf(" -mode mode : Mode string to pass into VixDiskLib_ConnectEx. "
	        "Valid modes are: nbd, nbdssl, san, hotadd \n");
    printf(" -thumb string : Provides a SSL thumbprint string for validation. "
           "Format: xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx\n");
    
    return 1;
}


/*
 *--------------------------------------------------------------------------
 *
 * main --
 *
 *      Main routine of the program.
 *
 * Results:
 *      None.
 *
 * Side effects:
 *      None.
 *
 *--------------------------------------------------------------------------
 */

int
main(int argc, char* argv[])
{
    int retval;
    bool bVixInit(false);

    memset(&appGlobals, 0, sizeof appGlobals);
    appGlobals.command = 0;
    appGlobals.adapterType = VIXDISKLIB_ADAPTER_SCSI_LSILOGIC;
    appGlobals.diskType = VIXDISKLIB_DISK_MONOLITHIC_SPARSE;
    appGlobals.startSector = 0;
    appGlobals.numSectors = 1;
    appGlobals.mbSize = 100;
    appGlobals.filler = 0xff;
    appGlobals.openFlags = 0;
    appGlobals.numThreads = 1;
    appGlobals.success = TRUE;
    appGlobals.isRemote = FALSE;
    appGlobals.cfgFile = NULL;

    retval = ParseArguments(argc, argv);
    if (retval) {
        return retval;
    }

	// Initialize random generator
    struct timeval time;
    gettimeofday(&time, NULL);

    srand((time.tv_sec * 1000) + (time.tv_usec/1000));

    VixDiskLibConnectParams cnxParams = {0};
    VixError vixError;
    try {
       if (appGlobals.isRemote) {
          cnxParams.vmxSpec = appGlobals.vmxSpec;
          cnxParams.serverName = appGlobals.host;
          cnxParams.credType = VIXDISKLIB_CRED_UID;
          cnxParams.creds.uid.userName = appGlobals.userName;
          cnxParams.creds.uid.password = appGlobals.password;
          cnxParams.thumbPrint = appGlobals.thumbPrint;
          cnxParams.port = appGlobals.port;
       }

       if (appGlobals.useInitEx) {
          vixError = VixDiskLib_InitEx(VIXDISKLIB_VERSION_MAJOR,
                                       VIXDISKLIB_VERSION_MINOR,
                                       &LogFunc, &WarnFunc, &PanicFunc,
                                       appGlobals.libdir,
                                       appGlobals.cfgFile);
       } else {
          vixError = VixDiskLib_Init(VIXDISKLIB_VERSION_MAJOR,
                                     VIXDISKLIB_VERSION_MINOR,
                                     NULL, NULL, NULL, // Log, warn, panic
                                     appGlobals.libdir);
       }
       CHECK_AND_THROW(vixError);
       bVixInit = true;

       if (appGlobals.vmxSpec != NULL) {
          vixError = VixDiskLib_PrepareForAccess(&cnxParams, "Sample");
          CHECK_AND_THROW(vixError);
       }
       if (appGlobals.ssMoRef == NULL && appGlobals.transportModes == NULL) {
          vixError = VixDiskLib_Connect(&cnxParams,
                                        &appGlobals.connection);
       } else {
          Bool ro = (appGlobals.openFlags & VIXDISKLIB_FLAG_OPEN_READ_ONLY);
          vixError = VixDiskLib_ConnectEx(&cnxParams, ro, appGlobals.ssMoRef,
                                          appGlobals.transportModes,
                                          &appGlobals.connection);
       }
       CHECK_AND_THROW(vixError);
        if (appGlobals.command & COMMAND_INFO) {
            DoInfo();
        } else if (appGlobals.command & COMMAND_CREATE) {
            DoCreate();
        } else if (appGlobals.command & COMMAND_REDO) {
            DoRedo();
        } else if (appGlobals.command & COMMAND_FILL) {
            DoFill();
        } else if (appGlobals.command & COMMAND_DUMP) {
            DoDump();
        } else if (appGlobals.command & COMMAND_READ_META) {
            DoReadMetadata();
        } else if (appGlobals.command & COMMAND_WRITE_META) {
            DoWriteMetadata();
        } else if (appGlobals.command & COMMAND_DUMP_META) {
            DoDumpMetadata();
        } else if (appGlobals.command & COMMAND_MULTITHREAD) {
            DoTestMultiThread();
        } else if (appGlobals.command & COMMAND_CLONE) {
            DoClone();
        } else if (appGlobals.command & COMMAND_READBENCH) {
            DoRWBench(true);
        } else if (appGlobals.command & COMMAND_WRITEBENCH) {
            DoRWBench(false);
	} else if (appGlobals.command & COMMAND_CHECKREPAIR) {
	    DoCheckRepair(appGlobals.repair);
	} else if (appGlobals.command & COMMAND_MOUNTDISK) {
	    DoMountDisk();
	} else if (appGlobals.command & COMMAND_CONVERT) {
	    DoConvert();
	}
        retval = 0;
    } catch (const VixDiskLibErrWrapper& e) {
       cout << "Error: [" << e.File() << ":" << e.Line() << "]  " <<
               std::hex << e.ErrorCode() << " " << e.Description() << "\n";
       retval = 1;
    }

    if (appGlobals.vmxSpec != NULL) {
       vixError = VixDiskLib_EndAccess(&cnxParams, "Sample");
    }
    if (appGlobals.connection != NULL) {
       VixDiskLib_Disconnect(appGlobals.connection);
    }
    if (bVixInit) {
       VixDiskLib_Exit();
    }
    return retval;
}


/*
 *--------------------------------------------------------------------------
 *
 * ParseArguments --
 *
 *      Parses the arguments passed on the command line.
 *
 * Results:
 *      None.
 *
 * Side effects:
 *      None.
 *
 *--------------------------------------------------------------------------
 */

static int
ParseArguments(int argc, char* argv[])
{
    int i;
    if (argc < 3) {
        printf("Error: Too few arguments. See usage below.\n\n");
        return PrintUsage();
    }
    for (i = 1; i < argc - 1; i++) {
        if (!strcmp(argv[i], "-info")) {
            appGlobals.command |= COMMAND_INFO;
            appGlobals.openFlags |= VIXDISKLIB_FLAG_OPEN_READ_ONLY;
        } else if (!strcmp(argv[i], "-create")) {
            appGlobals.command |= COMMAND_CREATE;
        } else if (!strcmp(argv[i], "-dump")) {
            appGlobals.command |= COMMAND_DUMP;
            appGlobals.openFlags |= VIXDISKLIB_FLAG_OPEN_READ_ONLY;
        } else if (!strcmp(argv[i], "-fill")) {
            appGlobals.command |= COMMAND_FILL;
        } else if (!strcmp(argv[i], "-meta")) {
            appGlobals.command |= COMMAND_DUMP_META;
            appGlobals.openFlags |= VIXDISKLIB_FLAG_OPEN_READ_ONLY;
        } else if (!strcmp(argv[i], "-single")) {
            appGlobals.openFlags |= VIXDISKLIB_FLAG_OPEN_SINGLE_LINK;
        } else if (!strcmp(argv[i], "-adapter")) {
            if (i >= argc - 2) {
                printf("Error: The -adapter option requires the adapter type "
                       "to be specified. The type must be 'ide' or 'scsi'. "
                       "See usage below.\n\n");
                return PrintUsage();
            }
            ++i;
            printf("%s\n", argv[i]);
            if (strcmp(argv[i], "ide") == 0) {
                appGlobals.adapterType = VIXDISKLIB_ADAPTER_IDE;
            }
            else if (strcmp(argv[i], "scsi") == 0) {
                appGlobals.adapterType = VIXDISKLIB_ADAPTER_SCSI_BUSLOGIC;
            }
            else {
                appGlobals.adapterType = VIXDISKLIB_ADAPTER_SCSI_LSILOGIC;
            }
        } else if (!strcmp(argv[i], "-disktype")) {
            if (i >= argc - 2) {
                printf("Error: The -disktype option requires the disk type "
                       "to be specified. See usage below.\n\n");
                return PrintUsage();
            }
            ++i;
            int type = atoi(argv[i]);
            if (type >= 1 && type <= 6) {
                appGlobals.diskType = (VixDiskLibDiskType)(type);
            }
        } else if (!strcmp(argv[i], "-mount")) {
            appGlobals.command |= COMMAND_MOUNTDISK;
        } else if (!strcmp(argv[i], "-rmeta")) {
           appGlobals.command |= COMMAND_READ_META;
           if (i >= argc - 2) {
               printf("Error: The -rmeta command requires a key value to "
                    "be specified. See usage below.\n\n");
               return PrintUsage();
           }
           appGlobals.metaKey = argv[++i];
               appGlobals.openFlags |= VIXDISKLIB_FLAG_OPEN_READ_ONLY;
        } else if (!strcmp(argv[i], "-wmeta")) {
            appGlobals.command |= COMMAND_WRITE_META;
            if (i >= argc - 3) {
                printf("Error: The -wmeta command requires key and value to "
                       "be specified. See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.metaKey = argv[++i];
            appGlobals.metaVal = argv[++i];
        } else if (!strcmp(argv[i], "-redo")) {
            if (i >= argc - 2) {
                printf("Error: The -redo command requires the parentPath to "
                       "be specified. See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.command |= COMMAND_REDO;
            appGlobals.parentPath = argv[++i];
        } else if (!strcmp(argv[i], "-val")) {
            if (i >= argc - 2) {
                printf("Error: The -val option requires a byte value to "
                       "be specified. See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.filler = strtol(argv[++i], NULL, 0);
        } else if (!strcmp(argv[i], "-start")) {
            if (i >= argc - 2) {
                printf("Error: The -start option requires a sector number to "
                       "be specified. See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.startSector = strtol(argv[++i], NULL, 0);
        } else if (!strcmp(argv[i], "-count")) {
            if (i >= argc - 2) {
                printf("Error: The -count option requires the number of "
                       "sectors to be specified. See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.numSectors = strtol(argv[++i], NULL, 0);
        } else if (!strcmp(argv[i], "-cap")) {
            if (i >= argc - 2) {
                printf("Error: The -cap option requires the capacity in MB "
                       "to be specified. See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.mbSize = strtol(argv[++i], NULL, 0);
        } else if (!strcmp(argv[i], "-clone")) {
            if (i >= argc - 2) {
                printf("Error: The -clone command requires the path of the "
                       "source vmdk to be specified. See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.srcPath = argv[++i];
            appGlobals.command |= COMMAND_CLONE;
        } else if (!strcmp(argv[i], "-convert")) {
            if (i >= argc - 2) {
                printf("Error: The -convert command requires the path of the "
                       "source raw image to be specified. See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.srcPath = argv[++i];
            appGlobals.command |= COMMAND_CONVERT;
        } else if (!strcmp(argv[i], "-readbench")) {
            if (0 && i >= argc - 2) {
                printf("Error: The -readbench command requires a block size "
                       "(in sectors) to be specified. See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.bufSize = strtol(argv[++i], NULL, 0);
            appGlobals.command |= COMMAND_READBENCH;
            appGlobals.openFlags |= VIXDISKLIB_FLAG_OPEN_READ_ONLY;
        } else if (!strcmp(argv[i], "-writebench")) {
            if (i >= argc - 2) {
                printf("Error: The -writebench command requires a block size "
                       "(in sectors) to be specified. See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.bufSize = strtol(argv[++i], NULL, 0);
            appGlobals.command |= COMMAND_WRITEBENCH;
        } else if (!strcmp(argv[i], "-multithread")) {
            if (i >= argc - 2) {
                printf("Error: The -multithread option requires the number "
                       "of threads to be specified. See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.command |= COMMAND_MULTITHREAD;
            appGlobals.numThreads = strtol(argv[++i], NULL, 0);
            appGlobals.openFlags |= VIXDISKLIB_FLAG_OPEN_READ_ONLY;
        } else if (!strcmp(argv[i], "-host")) {
            if (i >= argc - 2) {
                printf("Error: The -host option requires the IP address "
                       "or name of the host to be specified. "
                       "See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.host = argv[++i];
            appGlobals.isRemote = TRUE;
        } else if (!strcmp(argv[i], "-user")) {
            if (i >= argc - 2) {
                printf("Error: The -user option requires a username "
                       "to be specified. See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.userName = argv[++i];
            appGlobals.isRemote = TRUE;
        } else if (!strcmp(argv[i], "-password")) {
            if (i >= argc - 2) {
                printf("Error: The -password option requires a password "
                       "to be specified. See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.password = argv[++i];
            appGlobals.isRemote = TRUE;
        } else if (!strcmp(argv[i], "-thumb")) {
            if (i >= argc - 2) {
                printf("Error: The -thumb option requires an SSL thumbprint "
                       "to be specified. See usage below.\n\n");
               return PrintUsage();
            }
            appGlobals.thumbPrint = argv[++i];
            appGlobals.isRemote = TRUE;
        } else if (!strcmp(argv[i], "-port")) {
            if (i >= argc - 2) {
                printf("Error: The -port option requires the host's port "
                       "number to be specified. See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.port = strtol(argv[++i], NULL, 0);
            appGlobals.isRemote = TRUE;
        } else if (!strcmp(argv[i], "-vm")) {
            if (i >= argc - 2) {
                printf("Error: The -vm option requires the moref id of "
                       "the vm to be specified. See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.vmxSpec = argv[++i];
            appGlobals.isRemote = TRUE;
        } else if (!strcmp(argv[i], "-libdir")) {
           if (i >= argc - 2) {
              printf("Error: The -libdir option requires the folder location "
                     "of the VDDK installation to be specified. "
                     "See usage below.\n\n");
              return PrintUsage();
           }
           appGlobals.libdir = argv[++i];
        } else if (!strcmp(argv[i], "-initex")) {
           if (i >= argc - 2) {
              printf("Error: The -initex option requires the path and filename "
                     "of the VDDK config file to be specified. "
                     "See usage below.\n\n");
              return PrintUsage();
           }
           appGlobals.useInitEx = true;
           appGlobals.cfgFile = argv[++i];
           if (appGlobals.cfgFile[0] == '\0') {
              appGlobals.cfgFile = NULL;
           }
        } else if (!strcmp(argv[i], "-ssmoref")) {
           if (i >= argc - 2) {
              printf("Error: The -ssmoref option requires the moref id "
                       "of a VM snapshot to be specified. "
                       "See usage below.\n\n");
              return PrintUsage();
           }
           appGlobals.ssMoRef = argv[++i];
        } else if (!strcmp(argv[i], "-mode")) {
            if (i >= argc - 2) {
                printf("Error: The -mode option requires a mode string to  "
                       "connect to VixDiskLib_ConnectEx. Valid modes are "
                        "'nbd', 'nbdssl', 'san' and 'hotadd'. "
                        "See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.transportModes = argv[++i];
        } else if (!strcmp(argv[i], "-check")) {
            if (i >= argc - 2) {
                printf("Error: The -check command requires a true or false "
                       "value to indicate if a repair operation should be "
                       "attempted. See usage below.\n\n");
                return PrintUsage();
            }
            appGlobals.command |= COMMAND_CHECKREPAIR;
            appGlobals.repair = strtol(argv[++i], NULL, 0);
        } else {
           printf("Error: Unknown command or option: %s\n", argv[i]);
           return PrintUsage();
        }
    }
    appGlobals.diskPath = argv[i];

    if (BitCount(appGlobals.command) != 1) {
       printf("Error: Missing command. See usage below.\n");
       return PrintUsage();
    }

    if (appGlobals.isRemote) {
       if (appGlobals.host == NULL ||
           appGlobals.userName == NULL ||
           appGlobals.password == NULL) {
           printf("Error: Missing a mandatory option. ");
           printf("-host, -user and -password must be specified. ");
           printf("See usage below.\n");
           return PrintUsage();
       }
    }

    /*
     * TODO: More error checking for params, really
     */
    return 0;
}


/*
 *--------------------------------------------------------------------------
 *
 * DoInfo --
 *
 *      Queries the information of a virtual disk.
 *
 * Results:
 *      None.
 *
 * Side effects:
 *      None.
 *
 *--------------------------------------------------------------------------
 */

static void
DoInfo(void)
{
    VixDisk disk(appGlobals.connection, appGlobals.diskPath, appGlobals.openFlags);
    VixDiskLibInfo *info = NULL;
    VixError vixError;

    vixError = VixDiskLib_GetInfo(disk.Handle(), &info);

    CHECK_AND_THROW(vixError);

    cout << "capacity          = " << info->capacity << " sectors" << endl;
    cout << "number of links   = " << info->numLinks << endl;
    cout << "adapter type      = ";
    switch (info->adapterType) {
    case VIXDISKLIB_ADAPTER_IDE:
       cout << "IDE" << endl;
       break;
    case VIXDISKLIB_ADAPTER_SCSI_BUSLOGIC:
       cout << "BusLogic SCSI" << endl;
       break;
    case VIXDISKLIB_ADAPTER_SCSI_LSILOGIC:
       cout << "LsiLogic SCSI" << endl;
       break;
    default:
       cout << "unknown" << endl;
       break;
    }

    cout << "BIOS geometry     = " << info->biosGeo.cylinders <<
       "/" << info->biosGeo.heads << "/" << info->biosGeo.sectors << endl;

    cout << "physical geometry = " << info->physGeo.cylinders <<
       "/" << info->physGeo.heads << "/" << info->physGeo.sectors << endl;

    VixDiskLib_FreeInfo(info);

    cout << "Transport modes supported by vixDiskLib: " <<
       VixDiskLib_ListTransportModes() << endl;
}


/*
 *--------------------------------------------------------------------------
 *
 * DoCreate --
 *
 *      Creates a virtual disk.
 *
 * Results:
 *      None.
 *
 * Side effects:
 *      None.
 *
 *--------------------------------------------------------------------------
 */

static void
DoCreate(void)
{
   VixDiskLibCreateParams createParams;
   VixError vixError;

   createParams.adapterType = appGlobals.adapterType;

   createParams.capacity = appGlobals.mbSize * 2048;
   createParams.diskType = appGlobals.diskType;
   createParams.hwVersion = VIXDISKLIB_HWVERSION_WORKSTATION_5;

   vixError = VixDiskLib_Create(appGlobals.connection,
                                appGlobals.diskPath,
                                &createParams,
                                NULL,
                                NULL);
   CHECK_AND_THROW(vixError);
}


/*
 *--------------------------------------------------------------------------
 *
 * DoRedo --
 *
 *      Creates a child disk.
 *
 * Results:
 *      None.
 *
 * Side effects:
 *      None.
 *
 *--------------------------------------------------------------------------
 */

static void
DoRedo(void)
{
   VixError vixError;
   VixDisk parentDisk(appGlobals.connection, appGlobals.parentPath, 0);
   vixError = VixDiskLib_CreateChild(parentDisk.Handle(),
                                     appGlobals.diskPath,
                                     VIXDISKLIB_DISK_MONOLITHIC_SPARSE,
                                     NULL, NULL);
   CHECK_AND_THROW(vixError);
}


/*
 *--------------------------------------------------------------------------
 *
 * DoFill --
 *
 *      Writes to a virtual disk.
 *
 * Results:
 *      None.
 *
 * Side effects:
 *      None.
 *
 *--------------------------------------------------------------------------
 */

static void
DoFill(void)
{
    VixDisk disk(appGlobals.connection, appGlobals.diskPath, appGlobals.openFlags);
    uint8 buf[VIXDISKLIB_SECTOR_SIZE];
    VixDiskLibSectorType startSector;

    memset(buf, appGlobals.filler, sizeof buf);

    for (startSector = 0; startSector < appGlobals.numSectors; ++startSector) {
       VixError vixError;
       vixError = VixDiskLib_Write(disk.Handle(),
                                   appGlobals.startSector + startSector,
                                   1, buf);
       CHECK_AND_THROW(vixError);
    }
}


/*
 *--------------------------------------------------------------------------
 *
 * DoReadMetadata --
 *
 *      Reads metadata from a virtual disk.
 *
 * Results:
 *      None.
 *
 * Side effects:
 *      None.
 *
 *--------------------------------------------------------------------------
 */

static void
DoReadMetadata(void)
{
    size_t requiredLen;
    VixDisk disk(appGlobals.connection, appGlobals.diskPath, appGlobals.openFlags);
    VixError vixError = VixDiskLib_ReadMetadata(disk.Handle(),
                                                appGlobals.metaKey,
                                                NULL, 0, &requiredLen);
    if (vixError != VIX_OK && vixError != VIX_E_BUFFER_TOOSMALL) {
        THROW_ERROR(vixError);
    }
    std::vector <char> val(requiredLen);
    vixError = VixDiskLib_ReadMetadata(disk.Handle(),
                                       appGlobals.metaKey,
                                       &val[0],
                                       requiredLen,
                                       NULL);
    CHECK_AND_THROW(vixError);
    cout << appGlobals.metaKey << " = " << &val[0] << endl;
}


/*
 *--------------------------------------------------------------------------
 *
 * DoWriteMetadata --
 *
 *      Writes metadata in a virtual disk.
 *
 * Results:
 *      None.
 *
 * Side effects:
 *      None.
 *
 *--------------------------------------------------------------------------
 */

static void
DoWriteMetadata(void)
{
    VixDisk disk(appGlobals.connection, appGlobals.diskPath, appGlobals.openFlags);
    VixError vixError = VixDiskLib_WriteMetadata(disk.Handle(),
                                                 appGlobals.metaKey,
                                                 appGlobals.metaVal);
    CHECK_AND_THROW(vixError);
}


/*
 *--------------------------------------------------------------------------
 *
 * DoDumpMetadata --
 *
 *      Dumps all the metadata.
 *
 * Results:
 *      None.
 *
 * Side effects:
 *      None.
 *
 *--------------------------------------------------------------------------
 */

static void
DoDumpMetadata(void)
{
    VixDisk disk(appGlobals.connection, appGlobals.diskPath, appGlobals.openFlags);
    char *key;
    size_t requiredLen;

    VixError vixError = VixDiskLib_GetMetadataKeys(disk.Handle(),
                                                   NULL, 0, &requiredLen);
    if (vixError != VIX_OK && vixError != VIX_E_BUFFER_TOOSMALL) {
       THROW_ERROR(vixError);
    }
    std::vector<char> buf(requiredLen);
    vixError = VixDiskLib_GetMetadataKeys(disk.Handle(), &buf[0], requiredLen, NULL);
    CHECK_AND_THROW(vixError);
    key = &buf[0];

    while (*key) {
        vixError = VixDiskLib_ReadMetadata(disk.Handle(), key, NULL, 0,
                                           &requiredLen);
        if (vixError != VIX_OK && vixError != VIX_E_BUFFER_TOOSMALL) {
           THROW_ERROR(vixError);
        }
        std::vector <char> val(requiredLen);
        vixError = VixDiskLib_ReadMetadata(disk.Handle(), key, &val[0],
                                           requiredLen, NULL);
        CHECK_AND_THROW(vixError);
        cout << key << " = " << &val[0] << endl;
        key += (1 + strlen(key));
    }
}


/*
 *--------------------------------------------------------------------------
 *
 * DoDump --
 *
 *      Dumps the content of a virtual disk.
 *
 * Results:
 *      None.
 *
 * Side effects:
 *      None.
 *
 *--------------------------------------------------------------------------
 */

static void
DoDump(void)
{
    VixDisk disk(appGlobals.connection, appGlobals.diskPath, appGlobals.openFlags);
    uint8 buf[VIXDISKLIB_SECTOR_SIZE];
    VixDiskLibSectorType i;

    for (i = 0; i < appGlobals.numSectors; i++) {
        VixError vixError = VixDiskLib_Read(disk.Handle(),
                                            appGlobals.startSector + i,
                                            1, buf);
        CHECK_AND_THROW(vixError);
        DumpBytes(buf, sizeof buf, 16);
    }
}


/*
 *--------------------------------------------------------------------------
 *
 * BitCount --
 *
 *      Counts all the bits set in an int.
 *
 * Results:
 *      Number of bits set to 1.
 *
 * Side effects:
 *      None.
 *
 *--------------------------------------------------------------------------
 */

static int
BitCount(int number)    // IN
{
    int bits = 0;
    while (number) {
        number = number & (number - 1);
        bits++;
    }
    return bits;
}


/*
 *----------------------------------------------------------------------
 *
 * DumpBytes --
 *
 *      Displays an array of n bytes.
 *
 * Results:
 *      None.
 *
 * Side effects:
 *      None.
 *
 *----------------------------------------------------------------------
 */

static void
DumpBytes(const unsigned char *buf,     // IN
          size_t n,                     // IN
          int step)                     // IN
{
   size_t lines = n / step;
   size_t i;

   for (i = 0; i < lines; i++) {
      int k, last;
      printf("%04"FMTSZ"x : ", i * step);
      for (k = 0; n != 0 && k < step; k++, n--) {
         printf("%02x ", buf[i * step + k]);
      }
      printf("  ");
      last = k;
      while (k --) {
         unsigned char c = buf[i * step + last - k - 1];
         if (c < ' ' || c >= 127) {
            c = '.';
         }
         printf("%c", c);
      }
      printf("\n");
   }
   printf("\n");
}


/*
 *----------------------------------------------------------------------
 *
 * CopyThread --
 *
 *       Copies a source disk to the given file.
 *
 * Results:
 *       0 if succeeded, 1 if not.
 *
 * Side effects:
 *      Creates a new disk; sets appGlobals.success to false if fails
 *
 *----------------------------------------------------------------------
 */

#define TASK_OK ((void*)0)
#define TASK_FAIL ((void*)1)

static void *
CopyThread(void *arg)
{
   ThreadData *td = (ThreadData *)arg;

    try {
      VixDiskLibSectorType i;
      VixError vixError;
      uint8 buf[VIXDISKLIB_SECTOR_SIZE];

      for (i = 0; i < td->numSectors; i ++) {
         vixError = VixDiskLib_Read(td->srcHandle, i, 1, buf);
         CHECK_AND_THROW(vixError);
         vixError = VixDiskLib_Write(td->dstHandle, i, 1, buf);
         CHECK_AND_THROW(vixError);
      }

    } catch (const VixDiskLibErrWrapper& e) {
       cout << "CopyThread (" << td->dstDisk << ")Error: " << e.ErrorCode()
            <<" " << e.Description();
        appGlobals.success = FALSE;
        return TASK_FAIL;
    }

    cout << "CopyThread to " << td->dstDisk << " succeeded.\n";
    return TASK_OK;
}


/*
 *----------------------------------------------------------------------
 *
 * PrepareThreadData --
 *
 *      Open the source and destination disk for multi threaded copy.
 *
 * Results:
 *      Fills in ThreadData in td.
 *
 * Side effects:
 *      None.
 *
 *----------------------------------------------------------------------
 */

static void
PrepareThreadData(VixDiskLibConnection &dstConnection,
                  ThreadData &td)
{
   VixError vixError;
   VixDiskLibCreateParams createParams;
   VixDiskLibInfo *info = NULL;
   string prefixName,randomFilename;

   prefixName = "/tmp/test";
   GenerateRandomFilename(prefixName, randomFilename);
   td.dstDisk = randomFilename;

   vixError = VixDiskLib_Open(appGlobals.connection,
                              appGlobals.diskPath,
                              appGlobals.openFlags,
                              &td.srcHandle);
   CHECK_AND_THROW(vixError);

   vixError = VixDiskLib_GetInfo(td.srcHandle, &info);
   CHECK_AND_THROW(vixError);
   td.numSectors = info->capacity;
   VixDiskLib_FreeInfo(info);

   createParams.adapterType = VIXDISKLIB_ADAPTER_SCSI_BUSLOGIC;
   createParams.capacity = td.numSectors;
   createParams.diskType = VIXDISKLIB_DISK_SPLIT_SPARSE;
   createParams.hwVersion = VIXDISKLIB_HWVERSION_WORKSTATION_5;

   vixError = VixDiskLib_Create(dstConnection, td.dstDisk.c_str(),
                                &createParams, NULL, NULL);
   CHECK_AND_THROW(vixError);

   vixError = VixDiskLib_Open(dstConnection, td.dstDisk.c_str(), 0,
                              &td.dstHandle);
   CHECK_AND_THROW(vixError);
}


/*
 *----------------------------------------------------------------------
 *
 * DoTestMultiThread --
 *
 *      Starts a given number of threads, each of which will copy the
 *      source disk to a temp. file.
 *
 * Results:
 *      None.
 *
 * Side effects:
 *      None.
 *
 *----------------------------------------------------------------------
 */

static void
DoTestMultiThread(void)
{
   VixDiskLibConnectParams cnxParams = { 0 };
   VixDiskLibConnection dstConnection;
   VixError vixError;
   vector<ThreadData> threadData(appGlobals.numThreads);
   int i;

   vixError = VixDiskLib_Connect(&cnxParams, &dstConnection);
   CHECK_AND_THROW(vixError);

   vector<pthread_t> threads(appGlobals.numThreads);

   for (i = 0; i < appGlobals.numThreads; i++) {
      PrepareThreadData(dstConnection, threadData[i]);
      pthread_create(&threads[i], NULL, &CopyThread, (void*)&threadData[i]);
   }
   for (i = 0; i < appGlobals.numThreads; i++) {
      void *hlp;
      pthread_join(threads[i], &hlp);
   }

   for (i = 0; i < appGlobals.numThreads; i++) {
      VixDiskLib_Close(threadData[i].srcHandle);
      VixDiskLib_Close(threadData[i].dstHandle);
      VixDiskLib_Unlink(dstConnection, threadData[i].dstDisk.c_str());
   }
   VixDiskLib_Disconnect(dstConnection);
   if (!appGlobals.success) {
      THROW_ERROR(VIX_E_FAIL);
   }
}


/*
 *----------------------------------------------------------------------
 *
 * CloneProgress --
 *
 *      Callback for the clone function.
 *
 * Results:
 *      None
 *
 * Side effects:
 *      None.
 *
 *----------------------------------------------------------------------
 */

static Bool
CloneProgressFunc(void * /*progressData*/,      // IN
                  int percentCompleted)         // IN
{
   cout << "Cloning : " << percentCompleted << "% Done" << "\r";
   return TRUE;
}


/*
 *----------------------------------------------------------------------
 *
 * DoClone --
 *
 *      Clones a local disk (possibly to an ESX host).
 *
 * Results:
 *      None.
 *
 * Side effects:
 *      None.
 *
 *----------------------------------------------------------------------
 */

static void
DoClone(void)
{
   VixDiskLibConnection srcConnection;
   VixDiskLibConnectParams cnxParams = { 0 };
   VixError vixError = VixDiskLib_Connect(&cnxParams, &srcConnection);
   CHECK_AND_THROW(vixError);

   /*
    *  Note : These createParams are ignored for remote case
    */

   VixDiskLibCreateParams createParams;
   createParams.adapterType = appGlobals.adapterType;
   createParams.capacity = appGlobals.mbSize * 2048;
   createParams.diskType = VIXDISKLIB_DISK_STREAM_OPTIMIZED;
   createParams.hwVersion = VIXDISKLIB_HWVERSION_WORKSTATION_5;

   vixError = VixDiskLib_Clone(appGlobals.connection,
                               appGlobals.diskPath,
                               srcConnection,
                               appGlobals.srcPath,
                               &createParams,
                               CloneProgressFunc,
                               NULL,   // clientData
                               TRUE);  // doOverWrite
   VixDiskLib_Disconnect(srcConnection);
   CHECK_AND_THROW(vixError);
   cout << "\n Done" << "\n";
}

/*
 *----------------------------------------------------------------------
 *
 * DoConvert --
 *
 *      Converts a local raw disk to vmdk
 *
 * Results:
 *      None.
 *
 * Side effects:
 *      None.
 *
 *----------------------------------------------------------------------
 */

static void
DoConvert(void)
{
   
   appGlobals.diskType = VIXDISKLIB_DISK_MONOLITHIC_SPARSE;
   DoCreate();
   VixError vixError;
   VixDisk disk(appGlobals.connection, appGlobals.diskPath, appGlobals.openFlags);

   VixDiskLibInfo* info = 0;
   setbuf(stdout, (char *)NULL);
   vixError = VixDiskLib_GetInfo(disk.Handle(), &info);
   CHECK_AND_THROW(vixError);
   unsigned char diskbuf[VIXDISKLIB_SECTOR_SIZE];
   FILE* fp = fopen(appGlobals.srcPath, "rb");
   if (fp == NULL) {
      printf("Problem reading input raw file");
      return;
   }

   for(size_t i = 0; i < info->capacity; i += 1)
   {
       size_t data = fread(diskbuf, VIXDISKLIB_SECTOR_SIZE, 1, fp);
       vixError = VixDiskLib_Write(disk.Handle(), i, data, diskbuf);
       CHECK_AND_THROW(vixError);
   }
   fclose(fp);

   VixDiskLib_FreeInfo(info);

   cout << "\n Done" << "\n";
}


/*
 *----------------------------------------------------------------------
 *
 * PrintStat --
 *
 *      Print performance statistics for read/write benchmarks.
 *
 * Results:
 *      None
 *
 * Side effects:
 *      None.
 *
 *----------------------------------------------------------------------
 */

static void
PrintStat(bool read,            // IN
          struct timeval start, // IN
          struct timeval end,   // IN
          uint32 numSectors)    // IN
{
   uint64 elapsed;
   uint32 speed;

   elapsed = ((uint64)end.tv_sec * 1000000 + end.tv_usec -
              ((uint64)start.tv_sec * 1000000 + start.tv_usec)) / 1000;
   if (elapsed == 0) {
      elapsed = 1;
   }
   speed = (1000 * VIXDISKLIB_SECTOR_SIZE * (uint64)numSectors) / (1024 * 1024 * elapsed);
   printf("%s %d MBytes in %d msec (%d MBytes/sec)\n", read ? "Read" : "Wrote",
          (uint32)(numSectors /(2048)), (uint32)elapsed, speed);
}


/*
 *----------------------------------------------------------------------
 *
 * InitBuffer --
 *
 *      Fill an array of uint32 with random values, to defeat any
 *      attempts to compress it.
 *
 * Results:
 *      None
 *
 * Side effects:
 *      None.
 *
 *----------------------------------------------------------------------
 */

static void
InitBuffer(uint32 *buf,     // OUT
           uint32 numElems) // IN
{
   int i;

   srand(time(NULL));

   for (i = 0; i < numElems; i++) {
      buf[i] = (uint32)rand();
   }
}


/*
 *----------------------------------------------------------------------
 *
 * DoRWBench --
 *
 *      Perform read/write benchmarks according to settings in
 *      appGlobals. Note that a write benchmark will destroy the data
 *      in the target disk.
 *
 * Results:
 *      None
 *
 * Side effects:
 *      None.
 *
 *----------------------------------------------------------------------
 */

static void
DoRWBench(bool read) // IN
{
   VixDisk disk(appGlobals.connection, appGlobals.diskPath, appGlobals.openFlags);
   size_t bufSize;
   uint8 *buf;
   VixDiskLibInfo *info;
   VixError err;
   uint32 maxOps, i;
   uint32 bufUpdate;
   struct timeval start, end, total;

   if (appGlobals.bufSize == 0) {
      appGlobals.bufSize = DEFAULT_BUFSIZE;
   }
   bufSize = appGlobals.bufSize * VIXDISKLIB_SECTOR_SIZE;

   buf = new uint8[bufSize];
   if (!read) {
      InitBuffer((uint32*)buf, bufSize / sizeof(uint32));
   }

   err = VixDiskLib_GetInfo(disk.Handle(), &info);
   if (VIX_FAILED(err)) {
      delete [] buf;
      throw VixDiskLibErrWrapper(err, __FILE__, __LINE__);
   }

   maxOps = info->capacity / appGlobals.bufSize;
   VixDiskLib_FreeInfo(info);

   printf("Processing %d buffers of %d bytes.\n", maxOps, (uint32)bufSize);

   gettimeofday(&total, NULL);
   start = total;
   bufUpdate = 0;
   for (i = 0; i < maxOps; i++) {
      VixError vixError;

      if (read) {
         vixError = VixDiskLib_Read(disk.Handle(),
                                    i * appGlobals.bufSize,
                                    appGlobals.bufSize, buf);
      } else {
         vixError = VixDiskLib_Write(disk.Handle(),
                                     i * appGlobals.bufSize,
                                     appGlobals.bufSize, buf);

      }
      if (VIX_FAILED(vixError)) {
         delete [] buf;
         throw VixDiskLibErrWrapper(vixError, __FILE__, __LINE__);
      }

      bufUpdate += appGlobals.bufSize;
      if (bufUpdate >= BUFS_PER_STAT) {
         gettimeofday(&end, NULL);
         PrintStat(read, start, end, bufUpdate);
         start = end;
         bufUpdate = 0;
      }
   }
   gettimeofday(&end, NULL);
   PrintStat(read, total, end, appGlobals.bufSize * maxOps);
   delete [] buf;
}


/*
 *----------------------------------------------------------------------
 *
 * DoCheckRepair --
 *
 *      Check a sparse disk for internal consistency.
 *
 * Results:
 *      None
 *
 * Side effects:
 *      None.
 *
 *----------------------------------------------------------------------
 */

static void
DoCheckRepair(Bool repair)
{
   VixError err;

   err = VixDiskLib_CheckRepair(appGlobals.connection, appGlobals.diskPath,
                                repair);
   if (VIX_FAILED(err)) {
      throw VixDiskLibErrWrapper(err, __FILE__, __LINE__);
   }
}

/*
*----------------------------------------------------------------------
*
* DoMountDisk --
*
*      Mounts a vmdk to the specified path
*
* Results:
*      None
*
* Side effects:
*      None.
*
*----------------------------------------------------------------------
*/

static void
DoMountDisk()
{
   VixError err;
   const char *diskNames[1];
   diskNames[0] = appGlobals.diskPath;
   VixDiskSetHandle diskSetHandle = NULL;
   VixVolumeHandle *volumeHandles = NULL;
   VixVolumeInfo *volInfo = NULL;
   VixDiskSetInfo *diskSetInfo = NULL;
   size_t numVolumes = 0;

   // Init Mount Lib
   err = VixMntapi_Init(VIXMNTAPI_VERSION_MAJOR,
                  VIXMNTAPI_VERSION_MINOR,
		  NULL, NULL, NULL,
		  appGlobals.libdir,
		  appGlobals.cfgFile);
   CHECK_AND_THROW(err);
   // VixDisk disk(appGlobals.connection, appGlobals.diskPath, appGlobals.openFlags);

   // Open Disks
   err = VixMntapi_OpenDisks(appGlobals.connection, 
		       diskNames, 
		       1, appGlobals.openFlags, &diskSetHandle);
   CHECK_AND_THROW(err);
   err = VixMntapi_GetDiskSetInfo(diskSetHandle, &diskSetInfo);
   CHECK_AND_THROW(err);
   setbuf(stdout, (char *)NULL);
   printf("%s",
          diskSetInfo->mountPath);

   err = VixMntapi_GetVolumeHandles(diskSetHandle,
                                         &numVolumes,
                                         &volumeHandles);
   CHECK_AND_THROW(err);
   
   volInfo = NULL;
   err = VixMntapi_MountVolume(volumeHandles[0], FALSE);
   CHECK_AND_THROW(err);

   err = VixMntapi_GetVolumeInfo(volumeHandles[0], &volInfo);
   CHECK_AND_THROW(err);

   // printf("Type %d, isMounted %d, symLink %s, numGuestMountPoints %d\n",
   //       volInfo->type, volInfo->isMounted,
   //       volInfo->symbolicLink == NULL ? "<null>" : volInfo->symbolicLink,
   //       (int)volInfo->numGuestMountPoints);


   VixMntapi_FreeVolumeInfo(volInfo);
   VixMntapi_DismountVolume(volumeHandles[0], TRUE);

   VixMntapi_FreeDiskSetInfo(diskSetInfo);
   if (volumeHandles) {
      VixMntapi_FreeVolumeHandles(volumeHandles);
   }
   if (diskSetHandle) {
      VixMntapi_CloseDiskSet(diskSetHandle);
   }
   VixMntapi_Exit();
}


