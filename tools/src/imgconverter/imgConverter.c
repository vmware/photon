/*
Copyright 2015 VMware, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

/*
VMDK spec reference
https://www.vmware.com/support/developer/vddk/vmdk_50_technote.pdf

StreamOptimized format

Sparse header
Embedded descriptor
Grain marker
Compressed grain
...
Grain table marker
Grain table
Grain marker
Compressed grain
...
Grain table marker
Grain table
[ ... ]
Grain directory marker
Grain directory
Footer marker
Footer
End-of-stream marker

VHD spec reference
https://technet.microsoft.com/en-us/virtualization/bb676673.aspx?f=255&MSPPError=-2147217396

Hard disk footer fields	Size (bytes)
Cookie	8
Features	4
File Format Version	4
Data Offset	8
Time Stamp	4
Creator Application	4
Creator Version	4
Creator Host OS	4
Original Size	8
Current Size	8
Disk Geometry	4
Disk Type	4
Checksum	4
Unique Id	16
Saved State	1
Reserved	427

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <inttypes.h>
#include <errno.h>
#include <stdint.h>
#include <malloc.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <zlib.h>
#include <fcntl.h>
#include <sys/user.h>
#include <uuid/uuid.h>

static char* input_file;
static char* output_file;
static int output_format;

typedef uint64_t sector_type;
typedef uint8_t Bool;

#define SPARSE_MAGICNUMBER 0x564d444b /* 'V' 'M' 'D' 'K' */
#define VHD_FIXED_COOKIE 0x636f6e6563746978 /* "conectix" */
#define VHD_DYNAMIC_COOKIE 0x6378737061727365 /* "cxsparse" */
#define VHD_CREATOR_APP 0x70686f74 /* "phot" */
typedef enum _grain_marker_type
{
MARKER_EOS = 0,
MARKER_GT = 1,
MARKER_GD = 2,
MARKER_FOOTER = 3,
} grain_marker_type;

#define DISK_SECTOR_SIZE 512
#define NUM_GTE_PER_GT 512
#define DISK_DEFAULT_GRAINSIZE 128
#define DISK_DEFAULT_GRAINSIZE_BYTES (DISK_DEFAULT_GRAINSIZE * DISK_SECTOR_SIZE)
#define GEOMETRY_HEADS 255
#define GEOMETRY_SECTORS 63
#define CONST64U(c) c##uLL
#define SPARSE_SINGLE_ENDLINE_SEQUENCE_CHAR   '\n'
#define SPARSE_DOUBLE_ENDLINE_SEQUENCE_CHAR1  '\r'
#define SPARSE_DOUBLE_ENDLINE_SEQUENCE_CHAR2  '\n'
#define SPARSE_NON_ENDLINE_CHAR               ' '
#define SPARSE_VERSION_INCOMPAT_FLAGS   3
#define SPARSE_GD_AT_END                CONST64U(0xFFFFFFFFFFFFFFFF)
#define SPARSEFLAG_VALID_NEWLINE_DETECTOR       (1 << 0)

#define SPARSEFLAG_COMPRESSED                   (1 << 16)
#define SPARSEFLAG_EMBEDDED_LBA                 (1 << 17)

#define SPARSEFLAG_NEW_DISK_DEFAULTS SPARSEFLAG_VALID_NEWLINE_DETECTOR

#define SPARSE_MIN_GRAINSIZE 8

#define CEILING(a, b) (((a) + (b) - 1) / (b))
#define ROUNDUP(a, b) (((a) + (b) - 1) / (b) * (b))

#define VHD_BLOCK_SIZE 2097152 // 2 MB
#define SECTOR_PAD_SIZE 7
#define FIXED_VHD_SIZE 512
#define DYNAMIC_VHD_SIZE 1024

#define SWAP16(val) \
        ( (((val) >> 8) & 0x00FF) | (((val) << 8) & 0xFF00) )
#define SWAP32(val) \
        ( (((val) >> 24) & 0x000000FF) | (((val) >>  8) & 0x0000FF00) | \
        (((val) <<  8) & 0x00FF0000) | (((val) << 24) & 0xFF000000) )
#define SWAP64(val) \
        ( (((val) >> 56) & 0x00000000000000FF) | (((val) >> 40) & 0x000000000000FF00) | \
        (((val) >> 24) & 0x0000000000FF0000) | (((val) >>  8) & 0x00000000FF000000) | \
        (((val) <<  8) & 0x000000FF00000000) | (((val) << 24) & 0x0000FF0000000000) | \
        (((val) << 40) & 0x00FF000000000000) | (((val) << 56) & 0xFF00000000000000) )

static sector_type byte_count = 0;

struct _sparse_extent_header
{
    uint32_t magicNumber;
    uint32_t version;
    uint32_t flags;
    sector_type capacity;
    sector_type grainSize;
    sector_type descriptorOffset;
    sector_type descriptorSize;
    uint32_t numGTEsPerGT;
    sector_type rgdOffset;
    sector_type gdOffset;
    sector_type overHead;
    Bool uncleanShutdown;
    char singleEndLineChar;
    char nonEndLineChar;
    char doubleEndLineChar1;
    char doubleEndLineChar2;
    uint16_t compressAlgorithm;
    uint8_t pad[433];
}__attribute__((__packed__));
typedef struct _sparse_extent_header sparse_extent_header;

struct _vhd_chs
{
	uint16_t cylinders;
	uint8_t  heads;
	uint8_t  sectors;
}__attribute__((__packed__));
typedef struct _vhd_chs vhd_chs;

struct _fixed_vhd_header {
  uint64_t  cookie;
  uint32_t  features;
  uint32_t  file_format_version;
  uint64_t  data_offset;
  uint32_t  timestamp;
  uint32_t  creator_application;
  uint32_t  creator_version;
  uint32_t  creator_host_os;
  uint64_t  original_size;
  uint64_t  current_size;
  vhd_chs  disk_geometry;
  uint32_t  disk_type;
  uint32_t  checksum;
  uuid_t    unique_id;
  char      saved_state;
  char      reserved[427];
}__attribute__((__packed__));
typedef struct _fixed_vhd_header fixed_vhd_header;

struct _dynamic_vhd_header {
  uint64_t      cookie;
  uint64_t  data_offset;
  uint64_t  table_offset;
  uint32_t  header_version;
  uint32_t  max_table_entries;
  uint32_t  block_size;
  uint32_t  checksum;
  uuid_t    parent_unique_id;
  uint32_t  parent_timestamp;
  uint32_t  reserved1;
  uint16_t      parent_unicode_name[256];
  char      parent_locator_entry[192];
  char      reserved2[256];
}__attribute__((__packed__));
typedef struct _dynamic_vhd_header dynamic_vhd_header;

struct _marker
{
    sector_type val;
    uint32_t size;
    union
    {
        uint32_t type;
        uint8_t data[0];
    } u;
}__attribute__((__packed__));
typedef struct _marker marker;

static sparse_extent_header* vmdk_header;
static uint32_t* grain_directory = NULL;
static uint32_t* current_gt = NULL;
static uint32_t current_gd_index = 0;
static FILE *ifp, *ofp;

int create_vhd();
int create_vmdk();
void print_usage();
int parse_args(int argc, char* argv []);
off_t file_size(FILE *fp);
void make_sparse_header();
void pad_to(uint32_t alignment);
void write_file(char* buffer, size_t size);
void* aligned_malloc(size_t size);
int write_grain(sector_type index, uint8_t* grain, size_t size);
void flush_current_grain_table();
void add_to_grain_table(sector_type index);
void write_marker(grain_marker_type type, sector_type size);
void write_footer();
vhd_chs calculate_chs(sector_type total_sectors);
uint32_t vhd_checksum(uint8_t *header_data, size_t header_size);
void write_fixed_vhd_header(sector_type sector_count, sector_type size);
void write_dynamic_vhd_header(uint32_t entries);

void* aligned_malloc(size_t size)
{
    void* buf = NULL;
    buf = memalign(PAGE_SIZE, size);
    return buf;
}

void print_usage()
{
    printf("Usage: imgconverter -i <input_raw_file> -v <output_format> -o <output_file> \n");
    printf("output_format: vhd OR vmdk\n");
}

int parse_args(int argc, char* argv[])
{
    int i;
    for (i = 1; i < argc - 1; i++)
    {
        if (!strcmp(argv[i], "-i"))
        {
            input_file = argv[++i];
        }
        else if (!strcmp(argv[i], "-o"))
        {
            output_file = argv[++i];
        }
        else if (!strcmp(argv[i], "-v"))
        {
            i++;
            if (!strcmp(argv[i], "vhd"))
            {
                output_format = 0;
            }
            else if (!strcmp(argv[i], "vmdk"))
            {
                output_format = 1;
            }
            else
            {
                printf("Unknown file format\n");
                return -1;
            }
        }
        else
        {
            printf("Invalid option\n");
            return -1;
        }
    }
    return 0;
}

off_t file_size(FILE *fp) 
{
    struct stat st;
    fstat(fileno(fp), &st);
    return st.st_size;
}

void make_sparse_header(sector_type in_sectors, sector_type descSize)
{
    vmdk_header = (sparse_extent_header *) calloc(1, sizeof(*vmdk_header));
    vmdk_header->magicNumber = SPARSE_MAGICNUMBER;
    vmdk_header->version = SPARSE_VERSION_INCOMPAT_FLAGS;
    vmdk_header->flags = SPARSEFLAG_NEW_DISK_DEFAULTS | SPARSEFLAG_EMBEDDED_LBA |
        SPARSEFLAG_COMPRESSED;
    vmdk_header->capacity = in_sectors;
    vmdk_header->grainSize = DISK_DEFAULT_GRAINSIZE;
    vmdk_header->descriptorOffset = descSize > 0 ? 1 : 0;
    vmdk_header->descriptorSize = descSize;
    vmdk_header->numGTEsPerGT = NUM_GTE_PER_GT;
    vmdk_header->rgdOffset = 0;
    vmdk_header->gdOffset = SPARSE_GD_AT_END;
    vmdk_header->overHead = ROUNDUP(1 + descSize, DISK_DEFAULT_GRAINSIZE);
    vmdk_header->uncleanShutdown = 0;
    vmdk_header->singleEndLineChar = SPARSE_SINGLE_ENDLINE_SEQUENCE_CHAR;
    vmdk_header->nonEndLineChar = SPARSE_NON_ENDLINE_CHAR;
    vmdk_header->doubleEndLineChar1 = SPARSE_DOUBLE_ENDLINE_SEQUENCE_CHAR1;
    vmdk_header->doubleEndLineChar2 = SPARSE_DOUBLE_ENDLINE_SEQUENCE_CHAR2;
    vmdk_header->compressAlgorithm = 1;
}

void write_file(char* buffer, size_t size)
{
    fwrite(buffer, sizeof(char), size, ofp);
    byte_count += size;
}

void pad_to(uint32_t alignment)
{
    sector_type pad_size = ROUNDUP(byte_count, alignment) - byte_count;
    if (pad_size > 0)
    {
        char* pad_buffer = (char *) calloc(1, pad_size);
        if (!pad_buffer)
        {
            printf("Memory allocation failed\n");
            return;
        }
        write_file(pad_buffer, pad_size);
        free(pad_buffer);
    }
}

Bool is_zero_grain(uint8_t* grain, uint32_t size)
{
    uint32_t i;
    for (i = 0; i < size; i++)
    {
        if (grain[i])
        {
            return 0;
        }
    }
    return 1;
}

void write_marker(grain_marker_type type, sector_type size)
{
    uint32_t metadata_marker = 0;
    write_file((char *) &size, sizeof(size));
    write_file((char *) &metadata_marker, sizeof(metadata_marker));
    write_file((char *) &type, sizeof(type));
    pad_to(DISK_SECTOR_SIZE);
}

void flush_current_grain_table()
{
    write_marker(MARKER_GT, CEILING(vmdk_header->numGTEsPerGT * sizeof(uint32_t), DISK_SECTOR_SIZE));
    grain_directory[current_gd_index] = CEILING(byte_count, DISK_SECTOR_SIZE);
    write_file((char *) current_gt, vmdk_header->numGTEsPerGT * sizeof(uint32_t));
    pad_to(DISK_SECTOR_SIZE);
    free(current_gt);
    current_gt = NULL;
}

void add_to_grain_table(sector_type index)
{
    sector_type grain_num = index / vmdk_header->grainSize;
    uint32_t gd_index = (uint32_t) (grain_num / vmdk_header->numGTEsPerGT);
    uint32_t gt_index = (uint32_t) (grain_num % vmdk_header->numGTEsPerGT);

    if (current_gt != NULL && gd_index != current_gd_index)
    {
        flush_current_grain_table(); // sets _currentGrainTable = NULL
    }

    if (current_gt == NULL)
    {
        current_gt = (uint32_t *) calloc(1, vmdk_header->numGTEsPerGT * sizeof(uint32_t));
        current_gd_index = gd_index;
    }

    current_gt[gt_index] = CEILING(byte_count, DISK_SECTOR_SIZE);
}

void write_footer()
{
    if (current_gt != NULL) {
        flush_current_grain_table();
    }
    sector_type num_gdes = CEILING(vmdk_header->capacity, vmdk_header->numGTEsPerGT * vmdk_header->grainSize);
    sector_type gd_size = CEILING(num_gdes * sizeof(uint32_t), DISK_SECTOR_SIZE);

    write_marker(MARKER_GD, gd_size);
    sector_type gd_offset = CEILING(byte_count, DISK_SECTOR_SIZE);
    write_file((char *) grain_directory, gd_size);
    pad_to(DISK_SECTOR_SIZE);

    /* Write footer (with correct GD offset) */
    write_marker(MARKER_FOOTER, 1);
    vmdk_header->gdOffset = gd_offset;
    write_file((char *) vmdk_header, sizeof (*vmdk_header));

    write_marker(MARKER_EOS, 0);
}

int write_grain(sector_type index, uint8_t* grain, uint32_t grainSizeBytes)
{
    if (is_zero_grain(grain, grainSizeBytes))
    {
        sleep(100); // wait for the buffer to be written to file
        return 0;
    }
    /*
    * Maximum .1% + 12 bytes expansion according to zlib manual.
    Approximating below
    */
    uint32_t max_size = grainSizeBytes + (grainSizeBytes >> 9) + 13;
    uLongf compress_size = max_size;
    char* cmp_buf = (char *) malloc(compress_size);
    if (!cmp_buf)
    {
        printf("Memory allocation failed\n");
        return -1;
    }
    int zlibError = compress((uint8_t*) cmp_buf, &compress_size, grain, grainSizeBytes);
    if (zlibError != 0) 
    {
        free(cmp_buf);
        printf("Compression failed\n");
        return -1;
    }
    if (compress_size >= max_size)
    {
        printf("Compression size larger than max\n");
        free(cmp_buf);
        return -1;
    }
    add_to_grain_table(index);
    write_file((char *) &index, sizeof(index));
    write_file((char *) &compress_size, sizeof(compress_size));
    write_file((char *) &cmp_buf, sizeof(compress_size));
    pad_to(DISK_SECTOR_SIZE);

    free(cmp_buf);
    return 0;
}

vhd_chs calculate_chs(sector_type total_sectors)
{
    vhd_chs chs;
    uint8_t heads, sectors_per_track;
    uint64_t cylinder_x_heads;
    //                  C      H     S
    if (total_sectors > 65535 * 16 * 255)
    {
       total_sectors = 65535 * 16 * 255;
    }
     
    if (total_sectors >= 65535 * 16 * 63)
    {
       sectors_per_track = 255;
       heads = 16;
       cylinder_x_heads = total_sectors / sectors_per_track;
    }
    else
    {
       sectors_per_track = 17;
       cylinder_x_heads = total_sectors / sectors_per_track;
     
       heads = (cylinder_x_heads + 1023) / 1024;
         
       if (heads < 4)
       {
          heads = 4;
       }
       if (cylinder_x_heads >= (heads * 1024) || heads > 16)
       {
          sectors_per_track = 31;
          heads = 16;
          cylinder_x_heads = total_sectors / sectors_per_track; 
       }
       if (cylinder_x_heads >= (heads * 1024))
       {
          sectors_per_track = 63;
          heads = 16;
          cylinder_x_heads = total_sectors / sectors_per_track;
       }
    }
    chs.cylinders = cylinder_x_heads / heads;
    chs.heads = heads;
    chs.sectors = sectors_per_track;
    return chs;
}

uint32_t vhd_checksum(uint8_t *header_data, size_t header_size)
{
    uint32_t checksum = 0;
    while (header_size--)
          {
    	checksum += *header_data++;
    }
    return ~checksum;
}

void write_fixed_vhd_header(sector_type sector_count, sector_type size)
{
    fixed_vhd_header *header = (fixed_vhd_header *) calloc(1, sizeof(fixed_vhd_header));
    header->cookie = SWAP64(VHD_FIXED_COOKIE);
    header->features = SWAP32(2);
    header->file_format_version = SWAP32(0x10000);
    header->data_offset = SWAP64((uint64_t)512);
    header->timestamp = 0;
    header->creator_application = SWAP32(VHD_CREATOR_APP);
    header->creator_version = SWAP32(0x1);
    header->creator_host_os = 0;
    header->original_size = SWAP64(size);
    header->current_size = SWAP64(size);
    vhd_chs chs = calculate_chs(sector_count);
    vhd_chs chs_swapped;
    chs_swapped.cylinders = SWAP16(chs.cylinders);
    chs_swapped.heads = chs.heads;
    chs_swapped.sectors = chs.sectors;
    header->disk_geometry = chs_swapped;
    header->disk_type = SWAP32(3);
    header->checksum = 0;
    uuid_generate((unsigned char *)&header->unique_id);
    header->saved_state = 0;
    uint32_t cs = vhd_checksum((uint8_t *)header, FIXED_VHD_SIZE);
    header->checksum = SWAP32(cs);
    write_file((char *) header, FIXED_VHD_SIZE);
    fseek(ofp, 0, SEEK_SET);
    write_file((char *) header, FIXED_VHD_SIZE);
    free(header);
}

void write_dynamic_vhd_header(uint32_t bat_entries)
{
    dynamic_vhd_header *header = (dynamic_vhd_header *) calloc(1, sizeof(dynamic_vhd_header));
    header->cookie = SWAP64(VHD_DYNAMIC_COOKIE);
    header->data_offset = SWAP64(0xFFFFFFFFFFFFFFFF);
    header->table_offset = SWAP64((uint64_t)(FIXED_VHD_SIZE + DYNAMIC_VHD_SIZE));
    header->header_version = SWAP32(0x00010000);
    header->max_table_entries = SWAP32(bat_entries);
    header->block_size = SWAP32(VHD_BLOCK_SIZE);
    uint32_t cs = vhd_checksum((uint8_t *)header, DYNAMIC_VHD_SIZE);
    header->checksum = SWAP32(cs);
    write_file((char *) header, DYNAMIC_VHD_SIZE);
    free(header);
}

int create_vhd()
{
    ifp = fopen(input_file, "rb");
    if (ifp == NULL)
    {
        printf("Cannot open input file!\n");
        return -1;
    }

    ofp = fopen(output_file, "wb");

    if (ofp == NULL)
    {
        printf("Cannot open output file!\n");
        return -1;
    }

    sector_type in_size = (sector_type) file_size(ifp);

    if (in_size < 512)
    {
        printf("File size < 512 bytes, exiting...\n");
        return -1;
    }

    sector_type in_sector_count = CEILING(in_size, DISK_SECTOR_SIZE);
    sector_type numentries_bat = CEILING(in_size, VHD_BLOCK_SIZE);
    sector_type numsectors_bat = CEILING(numentries_bat * sizeof(uint32_t), DISK_SECTOR_SIZE);

    sector_type begin_sector = ((FIXED_VHD_SIZE + DYNAMIC_VHD_SIZE) / DISK_SECTOR_SIZE) + numsectors_bat;
    fseek(ofp, begin_sector * DISK_SECTOR_SIZE, SEEK_SET);
    
    // start reading from input file
    uint8_t* read_buffer = (uint8_t *) calloc(1, VHD_BLOCK_SIZE);
    uint32_t* bat_buffer = (uint32_t *) calloc(1, numentries_bat * sizeof(uint32_t));
    char* padding = (char *) calloc(1, DISK_SECTOR_SIZE);
    if (!read_buffer || !bat_buffer || !padding)
    {
        printf("Memory allocation failed\n");
        return -1;
    }
    int read_count = 0;
    static const char zero_buffer[VHD_BLOCK_SIZE] = { 0 };
    memset(padding, 0xFF, DISK_SECTOR_SIZE);

    while (read_count < numentries_bat)
    {
        int data = fread(read_buffer, VHD_BLOCK_SIZE, 1, ifp);
        if (!data)
        {
            break;
        }

        if (!memcmp(zero_buffer, read_buffer, VHD_BLOCK_SIZE))
        {
            bat_buffer[read_count] = 0xffffffff;
            read_count++;
            continue;
        }
        uint32_t ofp_location = (uint32_t)(ftell(ofp));
        if (ofp_location % DISK_SECTOR_SIZE)
        {
            printf("Wrong sector boundary for %d\n", ofp_location);
	    free(read_buffer);
	    free(bat_buffer);
	    free(padding);
            fclose(ifp);
            fclose(ofp);
            return -1;
        }
        bat_buffer[read_count] = SWAP32((ofp_location / DISK_SECTOR_SIZE));
        write_file(padding, DISK_SECTOR_SIZE);
        write_file((char *)read_buffer, VHD_BLOCK_SIZE);
        read_count++;
        memset(read_buffer, 0, VHD_BLOCK_SIZE);
    }
    free(read_buffer);
    
    write_fixed_vhd_header(in_sector_count, in_size);
    write_dynamic_vhd_header(numentries_bat);
    write_file((char *)bat_buffer, numentries_bat * sizeof(uint32_t));

    free(bat_buffer);
    free(padding);
    fclose(ifp);
    fclose(ofp);
    return 0;
}

int create_vmdk()
{
    ifp = fopen(input_file, "rb");
    if (ifp == NULL)
    {
        printf("Cannot open input file!\n");
        return -1;
    }

    ofp = fopen(output_file, "wb");

    if (ofp == NULL)
    {
        printf("Cannot open output file!\n");
        return -1;
    }

    sector_type in_size = (sector_type)file_size(ifp);

    if (in_size < 512)
    {
        printf("File size < 512 bytes, exiting...\n");
        return -1;
    }

    sector_type in_sector_count = CEILING(in_size, DISK_SECTOR_SIZE);
    sector_type in_grain_count = CEILING(in_sector_count, DISK_DEFAULT_GRAINSIZE);
    sector_type in_grain_table_count = CEILING(in_grain_count, NUM_GTE_PER_GT);
    sector_type in_cylinder_count = CEILING(in_sector_count, (GEOMETRY_HEADS * GEOMETRY_SECTORS));

    char buffer[DISK_SECTOR_SIZE] = { '\0' };
    sprintf(buffer,
        "# Disk Descriptor File\n"
        "version = 1\n"
        "CID = fb183c20\n"
        "parentCID = ffffffff\n"
        "createType = \"streamOptimized\"\n"
        "# Extent description\n"
        "RDONLY %lu SPARSE \"photon-ova.vmdk\"\n"
        "# The Disk Data Base\n"
        "#DDB\n"
        "ddb.virtualHWVersion = \"7\"\n"
        "ddb.geometry.cylinders = \"%lu\"\n"
        "ddb.geometry.heads = \"255\"\n"
        "ddb.geometry.sectors = \"63\"\n"
        "ddb.adapterType = \"lsilogic\"\n"
        "ddb.toolsVersion = \"2147483647\"", in_sector_count, in_cylinder_count);
    size_t buffer_length = strlen(buffer);
    printf("%s\n", buffer);

    sector_type descSize = CEILING(buffer_length, DISK_SECTOR_SIZE);
    make_sparse_header(in_sector_count, descSize);

    uint32_t num_gdes = CEILING(vmdk_header->capacity, vmdk_header->grainSize * vmdk_header->numGTEsPerGT);
    uint32_t gd_size = num_gdes * sizeof(uint32_t);
    grain_directory = (uint32_t *) calloc(1, gd_size);

    write_file((char *) vmdk_header, sizeof(*vmdk_header));
    write_file(buffer, DISK_SECTOR_SIZE);
    uint32_t alignment = DISK_DEFAULT_GRAINSIZE * DISK_SECTOR_SIZE;
    pad_to(alignment);

    sector_type i = 0;
    sector_type capacity = vmdk_header->capacity;
    uint32_t grain_size = vmdk_header->grainSize;
    uint8_t* grain = (uint8_t *) aligned_malloc(grain_size * DISK_SECTOR_SIZE);
    if (!grain)
    {
        printf("Memory allocation failed\n");
        return -1;
    }
    for (i = 0; i < capacity; i++)
    {
        printf("%f percent done\n", (double)i / capacity * 100);
        uint32_t current_grain = grain_size;
        if (i + grain_size >= capacity)
        {
            current_grain = capacity - i;
        }
        if (!fread(grain, current_grain, DISK_SECTOR_SIZE, ifp))
        {
            free(grain);
            return -1;
        }
        int not_written = write_grain(i, grain, current_grain * DISK_SECTOR_SIZE);
        if (not_written)
        {
            printf("Error writing to file\n");
            free(grain);
            return -1;
        }
    }

    free(grain);
    write_footer();
    free(vmdk_header);
    free(grain_directory);
    fclose(ifp);
    fclose(ofp);

    return 0;
}

int main(int argc, char* argv[])
{
    if (argc < 7)
    {
        print_usage();
    }
    else
    {
        int status = 0;
        status = parse_args(argc, argv);
        if (status)
        {
            return status;
        }
        int conversion_status = 0;

        if (output_format == 1)
        {
            // conversion_status = create_vmdk();
            printf("This feature has not been implemented yet\n");
            return -1;
        }
        else
        {
            conversion_status = create_vhd();
        }
        if (!conversion_status)
        {
            return conversion_status;
        }
    }
    return 0;
}
