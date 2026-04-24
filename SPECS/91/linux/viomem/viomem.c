/*
 * *****************************************************************
 * Copyright (c) 2024 Broadcom. All Rights Reserved.
 * The term “Broadcom” refers solely to the Broadcom Inc.
 * corporate affiliate that distributes this software.
 * ******************************************************************
 */

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/device.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/mm.h>
#include <linux/slab.h>
#include <asm/uaccess.h>
#include <linux/vmalloc.h>
#include <linux/ioctl.h>

#define MAX_SIZE (8 * 1024 * 1024 * 1024ULL)  /* max size mmaped to userspace */
#define DEVICE_NAME "viomem"
#define CLASS_NAME "viomem"


/*
 * Any changes made to ioctldata and IOCTL_GET_PFN
 * should be made both in Kernel Driver and
 * Protocol header files
 */

#define IOCTL_GET_PFN 3
struct __attribute__((__packed__)) ioctldata {
    unsigned long offset;
    unsigned int array_size;
    unsigned long pfn[];
};


typedef struct viomem_ctx {
    struct class         *class;
    struct device        *device;
    int                   refcount;
    int                   major;
    void                 *sh_mem;
    unsigned long long    allocatedmem;
    struct mutex          lock;
} viomem_ctx;

static viomem_ctx gctx;
static unsigned long memsize_mb = 1024;
module_param(memsize_mb, ulong, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);


/*
 *---------------------------------------------------------------------------
 *
 * viomem_init_shmem_locked --
 *
 *     Initialize the global shared memory required for mmap
 *
 * Results:
 *      int
 *
 *---------------------------------------------------------------------------
 */

static int viomem_init_shmem_locked(void)
{
    if (gctx.sh_mem != NULL) {
        return 0;
    }

    gctx.sh_mem = vmalloc(memsize_mb * 1024 * 1024);
    if (gctx.sh_mem == NULL) {
        pr_info("viomem: failed in vmalloc\n");
        return -ENOMEM;
    }
    gctx.allocatedmem = memsize_mb * 1024 * 1024;
    return 0;
}


/*
 *---------------------------------------------------------------------------
 *
 * viomem_release --
 *
 *      Executed once the device is closed or released by userspace
 *
 *  @param inodep: pointer to struct inode
 *  @param filep: pointer to struct file
 * Results:
 *      int
 *
 *---------------------------------------------------------------------------
 */

static int viomem_release(struct inode *inodep, struct file *filep)
{
    mutex_lock(&gctx.lock);
    gctx.refcount--;
    pr_debug("viomem: refcount %u Device successfully closed\n", gctx.refcount);
    mutex_unlock(&gctx.lock);

    return 0;
}

/*
 *---------------------------------------------------------------------------
 *
 * viomem_open --
 *
 *      Executed once the device is opened.
 *
 *  @param inodep: pointer to struct inode
 *  @param filep: pointer to struct file
 * Results:
 *      int
 *
 *---------------------------------------------------------------------------
 */

static int viomem_open(struct inode *inodep, struct file *filep)
{
    int ret = 0;

    /* Only allow for SYS_ADMIN capability user to access the device .*/
    if (!capable(CAP_SYS_ADMIN)) {
        return -EACCES;
    }

    mutex_lock(&gctx.lock);

    /* Allocate the shared memory only if the device file is opened */
    ret = viomem_init_shmem_locked();
    if (ret != 0) {
        pr_info("viomem: failed to initialize the shared memory");
        goto out;
    }

    gctx.refcount++;
    pr_debug("viomem: refcount:%u Device opened\n", gctx.refcount);

out:
    mutex_unlock(&gctx.lock);
    return ret;
}


/*
 *---------------------------------------------------------------------------
 *
 * viomem_ioctl --
 *
 *      ioctl handler that implements only one command for obtaining the
 *      pfn for the slab memory
 *
 *  @param filep: pointer to struct file
 *  @param cmd: command for ioctl
 *  @param arg: Userspae argument
 *
 * Results:
 *      int
 *
 *---------------------------------------------------------------------------
 */

static long viomem_ioctl(struct file *filep, unsigned int cmd,
                         unsigned long arg)
{
    int i = 0, ret = 0;
    unsigned long pageoff = 0;
    struct ioctldata *datap = vmalloc(sizeof(struct ioctldata));

    if (datap == NULL) {
        pr_info("viomem: failed in allocation of memory in ioctl");
        ret = -ENOMEM;
        goto out;
    }

    pr_debug("viomem: ioctl cmd is %d", cmd);

    switch (cmd) {
        case IOCTL_GET_PFN:
            ret = copy_from_user(datap, (void*) arg, sizeof(struct ioctldata));
            if (ret != 0) {
                pr_info("viomem: failed in copy_from_user");
                goto out;
            }

            if (datap->array_size > (gctx.allocatedmem/PAGE_SIZE)) {
                pr_info("viomem: Invalid size of array %d", datap->array_size);
                ret = -EINVAL;
                goto out;
            }

            if (datap->offset > gctx.allocatedmem) {
                pr_info("viomem: Invalid offset for ioctl");
                ret = -EINVAL;
                goto out;
            }

            if (datap->offset % PAGE_SIZE != 0) {
                pr_info("viomem: start offset should be multiple of PAGE_SIZE: "
                        "%lu", datap->offset);
                ret = -EINVAL;
                goto out;
            }

            pageoff = datap->offset / PAGE_SIZE;
            pr_debug("viomem: offset %lu array_size %d pageoff %lu ",
                    datap->offset, datap->array_size, pageoff);
            for (i = 0; i < datap->array_size; i++,pageoff++) {

                void *ptrend = gctx.sh_mem + (pageoff << PAGE_SHIFT);
                if (ptrend >= (gctx.sh_mem + gctx.allocatedmem)) {
                    pr_info("viomem: memory off bounds");
                    ret = -EINVAL;
                    goto out;
                }

                unsigned long pfn = vmalloc_to_pfn(ptrend);
                struct ioctldata *userdatap = (struct ioctldata *) arg;
                pr_debug("viomem: page no %d to copy %lu", i, pfn);
                ret = copy_to_user((void *)(&userdatap->pfn[i]),
                                   &pfn, sizeof(pfn));
                if (ret != 0) {
                    pr_info("viomem: failed in copy_to_user");
                    goto out;
                }
            }
            break;

        default :
            pr_debug("viomem : Unhandled IOCTL command");
	    ret = -EINVAL;
    }

out:
    vfree(datap);
    return ret;
}


/*
 *---------------------------------------------------------------------------
 *
 * viomem_mmap --
 *
 *      mmap handler to map kernel space to user space
 *
 *  @param inodep: pointer to struct inode
 *  @param vma: pointer to struct vm_area_struct
 * Results:
 *      int
 *
 *---------------------------------------------------------------------------
 */

static int viomem_mmap(struct file *filp, struct vm_area_struct *vma)
{
    int ret = 0;
    unsigned long size = (unsigned long)(vma->vm_end - vma->vm_start);
    int npages, i;
    unsigned long vastart = vma->vm_start;
    unsigned long pageoff = vma->vm_pgoff;

    pr_debug("viomem: mmap , start = %lu end = %lu size = %lu pageoff %lu allocated %llu ",
             vma->vm_start, vma->vm_end, size, pageoff, gctx.allocatedmem );
    if (size > gctx.allocatedmem) {
        pr_info("viomem: mmap wrong length size %lu allocatedmem %llu \n", size,
                gctx.allocatedmem);
        ret = -EINVAL;
        goto out;
    }

    if (size % PAGE_SIZE != 0) {
        pr_info("viomem: mmap size is not page aligned\n");
        return -EINVAL;
    }

    npages = size / PAGE_SIZE;

    for (i = 0; i < npages; i++) {
        void *ptrend = gctx.sh_mem + (pageoff << PAGE_SHIFT);
        if (ptrend >= gctx.sh_mem + gctx.allocatedmem) {
            pr_info("viomem: memory off bounds");
            ret = -EINVAL;
            goto out;
        }
        unsigned long pfn = vmalloc_to_pfn(ptrend);
        ret = remap_pfn_range(vma, vastart, pfn, PAGE_SIZE, vma->vm_page_prot);
        if (ret != 0) {
            goto out;
        }
        pageoff++;
        vastart += PAGE_SIZE;
    }

out:
    return ret;
}


/* initialize our handlers */
static const struct file_operations viomem_fops = {
    .open = viomem_open,
    .release = viomem_release,
    .mmap = viomem_mmap,
    .unlocked_ioctl = viomem_ioctl,
    .owner = THIS_MODULE,
};


/*
 *---------------------------------------------------------------------------
 *
 * viomem_init --
 *
 *      Called when inserting the module
 *
 * Results:
 *      int
 *
 *---------------------------------------------------------------------------
*/

static int __init viomem_init(void)
{
    int ret = 0;

    pr_info("viomem: Module parameter memsize_mb %lu\n", memsize_mb);
    if ((memsize_mb * 1024 * 1024) > MAX_SIZE) {
        pr_info("viomem: Invalid size \n");
        ret = -EINVAL;
        return ret;
    }

    gctx.major = register_chrdev(0, DEVICE_NAME, &viomem_fops);
    if (gctx.major < 0) {
        pr_info("viomem: fail to register major number!");
        return gctx.major;
    }

    gctx.class = class_create(THIS_MODULE, CLASS_NAME);
    if (IS_ERR(gctx.class)){
        pr_info("viomem: failed to register device class");
        ret = PTR_ERR(gctx.class);
        goto error_class_create;
    }

    gctx.device = device_create(gctx.class, NULL, MKDEV(gctx.major, 0), NULL,
                                DEVICE_NAME);
    if (IS_ERR(gctx.device)) {
        pr_info("viomem: failed in device_create\n");
        ret = PTR_ERR(gctx.device);
        goto error_device_create;
    }

    mutex_init(&gctx.lock);

    return ret;

error_device_create:
    class_destroy(gctx.class);
error_class_create:
    unregister_chrdev(gctx.major, DEVICE_NAME);
    pr_info("viomem: Failed in init unregistered!");

    return ret;
}


/*
 *---------------------------------------------------------------------------
 *
 * viomem_exit --
 *
 *      Called when removing the module
 *
 * Results:
 *      void
 *
 *---------------------------------------------------------------------------
*/

static void __exit viomem_exit(void)
{
    mutex_lock(&gctx.lock);
    pr_info("viomem: unregistering refcount %d", gctx.refcount);
    if (gctx.refcount > 0) {
      pr_warn("Device is busy\n");
      mutex_unlock(&gctx.lock);
      return;
    }
    mutex_unlock(&gctx.lock);

    mutex_destroy(&gctx.lock);
    device_destroy(gctx.class, MKDEV(gctx.major, 0));
    class_destroy(gctx.class);
    unregister_chrdev(gctx.major, DEVICE_NAME);

    if (gctx.sh_mem != NULL) {
        vfree(gctx.sh_mem);
    }
    pr_info("viomem: unregistered!");
}

module_init(viomem_init);
module_exit(viomem_exit);
MODULE_LICENSE("GPL v2");
