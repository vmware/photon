/*
 * Kernel proxy module for managing access to jitterentropy.
 * Allocates and controls access to a limited number of jitterentropy
 * instances, instead of each process allocating their own ephemeral
 * instance(s).
 *
 * Copyright (C) 2024 Broadcom, Inc.
 * Author: Brennan Lamoreaux <brennan.lamoreaux@broadcom.com>
 */
#include <linux/init.h>
#include <linux/module.h>
#include <crypto/internal/rng.h>
#include <linux/semaphore.h>
#include <linux/mutex.h>
#include <linux/list.h>

static int max_jent_insts = 32;

struct jent_instance {
    struct crypto_rng *jent_inst;
    struct list_head list_entry;
    struct crypto_tfm *tfm;
    int failures;
};

static atomic_t module_is_exiting = ATOMIC_INIT(0);

/* Tracks number of currently pending allocations of new instances */
static int pending_allocs = 0;

/* Counter for the total number of currently allocated instances */
static int num_jent_instances = 0;

/* Head of list of free jent instances */
static struct jent_instance free_list_head;

/* Head of list of busy jent instances */
static struct jent_instance busy_list_head;

/* Deallocation work struct */
struct delayed_work dealloc_work;

/*
 * Mutex lock protection for the list of jitterentropy instances and related
 * metadata
 */
static struct mutex list_lock;

/*
 * Binary semaphore that acts as the queue for the incoming requests.
 * When there are no available instances, the semaphore is locked.
 * When an instance is free, the semaphore is unlocked.
 */
static DEFINE_SEMAPHORE(wait_queue);

bool is_empty(struct jent_instance *list_head) {
    bool ret;

    mutex_lock(&list_lock);
    ret = list_empty(&list_head->list_entry);
    mutex_unlock(&list_lock);

    return ret;
}

/*
 * If available, take a free instance from the end of the free list.
 * Move it to the busy list. Returns the newly busy instance, or NULL.
 * list_lock must be held by caller
 */
static struct jent_instance* get_free_instance(struct crypto_tfm *tfm) {
    struct jent_instance *ret_inst = NULL;
    if(!list_empty(&free_list_head.list_entry)) {
        ret_inst = list_last_entry(&free_list_head.list_entry,
                                    struct jent_instance,
                                    list_entry);
        ret_inst->tfm = tfm;
        list_del(&ret_inst->list_entry);
        list_add_tail(&ret_inst->list_entry, &busy_list_head.list_entry);
    }

    return ret_inst;
}

/* Assumes that instance is exclusively held (removed from any lists) */
static void dealloc_jent_instance(struct jent_instance *jent) {
    if(!jent)
        return;

    crypto_free_rng(jent->jent_inst);
    kfree(jent);
}

/*
 * Helper function for removing instance from pool. Called prior to
 * dealloc_jent_instance() with list_lock held.
 */
static void del_instance_from_pool(struct jent_instance *jent) {
    if(!jent)
        return;

    list_del(&jent->list_entry);

    if(num_jent_instances <= 0)
        WARN_ONCE(1, "deleting unaccounted for instance from pool!");
    else
        num_jent_instances--;
}

/* Shrink the number of free instances if appropriate */
static void deferred_dealloc(struct work_struct *work) {
    struct jent_instance *tmp = NULL;

    for(;;) {
        mutex_lock(&list_lock);
        if(!list_empty(&busy_list_head.list_entry) ||
            list_empty(&free_list_head.list_entry) ||
            list_is_singular(&free_list_head.list_entry)) {
            mutex_unlock(&list_lock);
            return;
        }

        tmp = list_last_entry(&free_list_head.list_entry,
                            struct jent_instance,
                            list_entry);

        if(!tmp){
            mutex_unlock(&list_lock);
            continue;
        }

        del_instance_from_pool(tmp);
        mutex_unlock(&list_lock);

        dealloc_jent_instance(tmp);
    }
}
DECLARE_DELAYED_WORK(dealloc_work, deferred_dealloc);

/*
 * Alloc a new instance. Returns a pointer to the new instance, or NULL on
 * failure.
 */
static struct jent_instance* alloc_jent_instance(void) {
    struct jent_instance *jent = kzalloc(sizeof(struct jent_instance),
                                         GFP_KERNEL);

    if(!jent) {
        pr_alert("Jitterentropy RNG Proxy: Failed to allocate memory for \
                  new instance\n");
        return NULL;
    }

    jent->jent_inst = crypto_alloc_rng("jitterentropy_rng-generic", 0, 0);
    if(IS_ERR(jent->jent_inst)) {
        pr_alert("Jitterentropy RNG Proxy: Failure during allocation of crypto \
                  RNG handle: %ld\n", PTR_ERR(jent->jent_inst));
        kfree(jent);
        return NULL;
    }

    INIT_LIST_HEAD(&jent->list_entry);

    return jent;
}

static void put_instance(struct jent_instance *jent_inst) {
    if(jent_inst) {
        mutex_lock(&list_lock);
        list_del(&jent_inst->list_entry);
        list_add_tail(&jent_inst->list_entry, &free_list_head.list_entry);

        jent_inst->tfm = NULL;
        up(&wait_queue);

        if(list_empty(&busy_list_head.list_entry) &&
            !list_is_singular(&free_list_head.list_entry)) {
            schedule_delayed_work(&dealloc_work, HZ);
        }
        mutex_unlock(&list_lock);
    }
}

/* Called by cleanup function. Puts back any instances with the calling tfm */
static void cleanup_dead_task(struct crypto_tfm *tfm) {
    struct jent_instance *inst;
    struct list_head *pos = NULL, *tmp = NULL;

    mutex_lock(&list_lock);
    list_for_each_safe(pos, tmp, &free_list_head.list_entry) {
        inst = list_entry(pos, struct jent_instance, list_entry);
        if(inst && inst->tfm == tfm)
            break;
        inst = NULL;
    }
    mutex_unlock(&list_lock);

    put_instance(inst);
}

/* Return a jitterentropy instance from the free list */
static struct jent_instance* get_instance(struct crypto_tfm *tfm) {
    int status = 0;
    struct jent_instance *new_inst = NULL, *ret_inst = NULL;

    /*
     * Fast path if no waiters on queue. list_lock must be held before
     * down_trylock(), so as to avoid up(&wait_queue) too many times.
     */
    mutex_lock(&list_lock);
    if(!down_trylock(&wait_queue)) {
        ret_inst = get_free_instance(tfm);

        if(!list_empty(&free_list_head.list_entry))
            up(&wait_queue);
    }
    mutex_unlock(&list_lock);

    while(!ret_inst) {
        /*
         * No deallocation while there's any pending reqs.
         * Let's just consume the extra instances until we run
         * out of requests.
         */
        cancel_delayed_work_sync(&dealloc_work);

        if(!atomic_read(&module_is_exiting)) {
            /*
             * If no instances yet, do allocation synchronously so as to avoid
             * any cases where we fail to alloc, yet some processes reach the
             * wait queue and get stuck forever.
             *
             * If we already have some instances, we can do alloc of new
             * ones asynchronously, making sure that we don't overshoot
             * the max number of instances.
             */
            mutex_lock(&list_lock);
            if(num_jent_instances == 0)
                new_inst = alloc_jent_instance();
            else if(pending_allocs + num_jent_instances < max_jent_insts) {
                pending_allocs++;
                mutex_unlock(&list_lock);

                new_inst = alloc_jent_instance();

                mutex_lock(&list_lock);
                pending_allocs--;
            }

             if(!new_inst && num_jent_instances == 0) {
                    mutex_unlock(&list_lock);
                    pr_err("Jitterentropy RNG Proxy: Failed to allocate first \
                            instance!\n");
                    return ERR_PTR(-EAGAIN);
            } else if(new_inst)
                num_jent_instances++;
            mutex_unlock(&list_lock);

            put_instance(new_inst);
        }

        /*
         * Join the back of the queue, or grab lock if unlocked.
         * All instances must be currently taken if we're waiting,
         * and so each waiter will be let through the queue in order that the
         * instances are released, or new ones are allocated.
         */
        status = down_interruptible(&wait_queue);
        if(status < 0) {
            pr_debug("Jitterentropy RNG Proxy: Interrupted while waiting for \
                    available instance!\n");
            return ERR_PTR(status);
        }


        /* Module is being unloaded, try again */
        if(atomic_read(&module_is_exiting)) {
            up(&wait_queue);
            return ERR_PTR(-EAGAIN);
        }

        mutex_lock(&list_lock);
        ret_inst = get_free_instance(tfm);
        mutex_unlock(&list_lock);
    }

    return ret_inst;
}

static int jent_proxy_generate_random(struct crypto_rng *tfm,
                                const u8 *src, unsigned int slen,
                                u8 *rdata, unsigned int dlen) {
    struct jent_instance *free_inst = NULL, *new_inst = NULL;
    int ret = 0;

    free_inst = get_instance(crypto_rng_tfm(tfm));
    if(IS_ERR(free_inst)){
        pr_debug("Jitterentropy RNG Proxy: Failed to grab a usable instance \
                  of jitterentropy!\n");
        return PTR_ERR(free_inst);
    }

    /* Call upon the chosen jitterentropy instance to get our random bits */
    ret = crypto_rng_get_bytes(free_inst->jent_inst, rdata, dlen);

    if(ret == -EFAULT)
        free_inst->failures = 3;
    else if(ret == -EINVAL)
        free_inst->failures++;
    else if(ret == 0)
        free_inst->failures = 0;

    if(ret < 0)
        ret = -EAGAIN;

    /* Three strikes and you're out! */
    if(free_inst->failures >= 3) {
        new_inst = alloc_jent_instance();

        mutex_lock(&list_lock);
        if(new_inst)
            num_jent_instances++;

        /*
         * Dealloc unhealthy instance if new alloc above was successful,
         * or we have more than 1 instance anyways. We should avoid the
         * situation where we dealloc the last instance without adding
         * a new one and leave the pool empty.
         */
        if(num_jent_instances > 1) {
            del_instance_from_pool(free_inst);
            mutex_unlock(&list_lock);

            dealloc_jent_instance(free_inst);
            free_inst = new_inst;
        } else
            mutex_unlock(&list_lock);
    }

    put_instance(free_inst);

    return ret;
}

static int jent_proxy_reset(struct crypto_rng *tfm,
                    const u8 *seed, unsigned int slen) {
    return 0;
}

static int jent_proxy_init(struct crypto_tfm *tfm) {
    /* Nothing to do here */
    return 0;
}

static void jent_proxy_cleanup(struct crypto_tfm *tfm) {
    /* Schedule cleanup in case of unexpected interrupt/exit */
    cleanup_dead_task(tfm);
    if(!is_empty(&free_list_head))
        schedule_delayed_work(&dealloc_work, HZ);

    return;
}

static struct rng_alg jent_proxy_alg = {
    .generate       = jent_proxy_generate_random,
    .seed           = jent_proxy_reset,
    .seedsize       = 0,
    .base           = {
        .cra_name               = "jitterentropy_rng",
        .cra_driver_name        = "jitterentropy_rng-proxy",
        .cra_priority           = 200,
        .cra_ctxsize            = sizeof(struct jent_instance),
        .cra_module             = THIS_MODULE,
        .cra_init               = jent_proxy_init,
        .cra_exit               = jent_proxy_cleanup,
    }
};

static int __init jent_proxy_mod_init(void) {
    int ret;

    if(max_jent_insts < 1) {
        pr_err("Jitterentropy RNG Proxy: Can't load proxy with a max of %d \
                instances! Check the value of max_jent_insts on the cmdline.\n",
                max_jent_insts);
        return -EINVAL;
    }

    /*
     * Lock wait_queue semaphore as there are no available instances at init
     * time. It will be unlocked when an instance becomes available.
     */
    ret = down_interruptible(&wait_queue);
    BUG_ON(ret < 0);

    mutex_init(&list_lock);

    INIT_LIST_HEAD(&free_list_head.list_entry);
    INIT_LIST_HEAD(&busy_list_head.list_entry);

    /*
     * Register our proxy crypto algo with the kernel.
     * This will allow clients to send us requests
     */
    ret = crypto_register_rng(&jent_proxy_alg);
    if(ret < 0) {
        pr_err("Jitterentropy RNG Proxy: Failed to register proxy: %d\n", ret);
        return ret;
    }

    return 0;
}

static void __exit jent_proxy_mod_exit(void) {
    struct list_head *pos = NULL, *tmp = NULL;
    struct jent_instance *inst = NULL;

    /* Unregister proxy handle, no new reqs can come in */
    crypto_unregister_rng(&jent_proxy_alg);

    cancel_delayed_work_sync(&dealloc_work);

    /* Wait for all pending reqs to complete */
    while(!is_empty(&busy_list_head) && down_trylock(&wait_queue));

    atomic_set(&module_is_exiting, 1);

    /* Free all instances */
    mutex_lock(&list_lock);
    list_for_each_safe(pos, tmp, &free_list_head.list_entry) {
        inst = list_entry(pos, struct jent_instance, list_entry);
        if(!inst)
            continue;

        del_instance_from_pool(inst);

        mutex_unlock(&list_lock);
        dealloc_jent_instance(inst);
        mutex_lock(&list_lock);
    }
    mutex_unlock(&list_lock);

    /* Unlock wait queue */
    up(&wait_queue);

}

module_init(jent_proxy_mod_init);
module_exit(jent_proxy_mod_exit);

module_param(max_jent_insts, int, 0444);
MODULE_PARM_DESC(max_jent_insts, "Maximum number of jitterentropy instances.");

MODULE_AUTHOR("Brennan Lamoreaux <brennan.lamoreaux@broadcom.com>");
MODULE_DESCRIPTION("Management proxy for Jitterentropy RNG");
MODULE_LICENSE("GPL");
