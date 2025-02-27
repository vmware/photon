# Handles cache operations, updating scan dir, etc
import common
from common import (
    strip_license_id,
    cleanup_license_expression,
    extract_top_level_expressions,
    pr_err,
)
import scancode_config
import os
import hashlib
import pathlib
import multiprocessing
import yaml
import shutil

try:
    import redis
except ImportError:
    pr_err("'redis' not found, please install with 'pip install redis'")
    raise


class CacheUtil:
    def __init__(self, redis_host, redis_port, redis_ttl):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_ttl = redis_ttl
        self.cached_spdx_ids = set()
        self.cached_licenses_info = {}
        # scan dir with only uncached files
        self._non_cached_scan_dir = f"{common.ph_scan_tool_dir}/non_cached_scan_dir"

        self._redis_cache = redis.Redis(
            host=redis_host, port=redis_port, decode_responses=True
        )

    # Convert file path to key (checksum)
    def _conv_filepath_to_key(self, file_path=None):
        sc_version = scancode_config.__version__
        checksum = None

        # compute checksum
        with open(file_path, "rb") as f_to_check:
            checksum = hashlib.file_digest(f_to_check, "md5").hexdigest()

        # Key for known failures should not be returned
        if checksum in common.known_failures:
            return None

        return f"{sc_version}-{checksum}"

    # multithreaded job which checks if the file is in the db already,
    # and if so, removes it from the scan dir
    def _db_cache_clear_job(
        self,
        manager=None,
        file_list=None,
        thread_cached_spdx_ids=None,
        thread_cached_license_info=None,
        thread_lock=None,
    ):
        key = ""
        keys = list()
        cached_results = None
        redis_pipeline = self._redis_cache.pipeline()

        for file in file_list:
            key = self._conv_filepath_to_key(file_path=os.path.abspath(file))

            # Skip files which are known to fail the scanner
            if not key:
                file_list.remove(file)
                pr_err(f"SKIP BAD FILE: {file}")
                continue

            keys.append(key)

            redis_pipeline.getex(key, ex=self.redis_ttl)

        cached_results = redis_pipeline.execute()

        # all these lists have the same order, so this is fine
        for key, res, file in zip(keys, cached_results, file_list):
            spdx_id = res

            # if nothing found for that key, we need to scan the file
            # must check specifically for None type here, otherwise this
            # will also trigger for blank license IDs
            if spdx_id is None:
                # in the majority of cases, after the very first scan,
                # the number of files which need scanning will be quite small.
                # So let's move only those files which need scanning to the scan
                # directory, instead of removing known files from the rpmbuild
                # directory. Worst case, we move the entire package source, but this
                # only happens on the very first scan. Subsequent scans should be
                # much faster and move only a couple files.
                new_path = os.path.join(self._non_cached_scan_dir, file.strip("/"))
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                shutil.move(file, new_path)
                continue

            # get the license info from the cache
            with thread_lock:
                # assume expression is already cleaned before we cached it
                # all individual license expressions should be comma separated
                for exp in spdx_id.split(","):
                    lic_id = strip_license_id(exp)
                    if lic_id not in thread_cached_license_info:
                        thread_cached_license_info[lic_id] = manager.list()
                    thread_cached_license_info[lic_id].append(file)
                    if exp != "NO-LICENSE":
                        thread_cached_spdx_ids[lic_id] = 1

    # after successful scan completion, update the database
    # with the data for these files
    def _add_scan_result_to_db(self, redis_pipeline=None, spdx_id=None, filepath=None):
        if not redis_pipeline or not filepath:
            return

        key = self._conv_filepath_to_key(file_path=os.path.abspath(filepath))

        # Redis doesn't like 'None'
        if not spdx_id:
            spdx_id = "NO-LICENSE"

        redis_pipeline.set(key, spdx_id, ex=self.redis_ttl)

    def add_all_scan_results_to_cache(
        self, scan_dir=None, yaml_fp=None, exceptions_list=[]
    ):

        redis_pipeline = None
        scancode_yaml = None
        cached_cleaned_results = {}
        spdx_exp = None

        if not yaml_fp:
            return

        with open(yaml_fp, "r") as scancode_yaml_f:
            scancode_yaml = yaml.load(scancode_yaml_f, Loader=yaml.SafeLoader)

        # Save file->license maps to the database
        redis_pipeline = self._redis_cache.pipeline()
        for file in scancode_yaml["files"]:
            # it's ok if this is None, some files may not have licenses
            spdx_exp = None
            file_detections = set()
            plib_path = pathlib.Path(file["path"])
            file_path = f"{scan_dir}/{pathlib.Path(*plib_path.parts[1:])}"

            if os.path.isdir(file_path):
                continue

            for detection in file["license_detections"]:
                after_cleaning = None
                before_cleaning = detection["license_expression_spdx"]
                if before_cleaning not in cached_cleaned_results:
                    after_cleaning = cleanup_license_expression(
                        common.ignore_list, exceptions_list, before_cleaning
                    )

                    # cache the result - likely in big packages there will be many
                    # of the same, for example, GPL licenses or such. Cleaning is
                    # expensive and time consuming, so avoid it if possible.
                    cached_cleaned_results[before_cleaning] = after_cleaning
                else:
                    after_cleaning = cached_cleaned_results[before_cleaning]

                for lic in extract_top_level_expressions(after_cleaning):
                    if lic:
                        file_detections.add(strip_license_id(lic))

            # Instead of using the whole expression, which is difficult to work
            # with, find the individual license expressions, and then separate them
            # by commas scancode likes to concatenate all with ANDs, so we get some
            # weird expressions like ((A AND B) AND C), which is hard to parse
            # (can't just split on AND). But the scancode yaml will give us two
            # separate ones: A AND B, and C. This same issue is not present in the
            # license_detections section above, which causes compatibility issues.
            spdx_exp = ",".join(file_detections)

            self._add_scan_result_to_db(redis_pipeline, spdx_exp, file_path)

        redis_pipeline.execute()

    # Move files which are not cached to the scan dir
    # multiprocess this to divide and conquer
    def populate_scan_dir(self, scan_dir=None):
        file_lists = list()
        git_files = [".gitignore", ".gitattributes"]

        manager = multiprocessing.Manager()
        thread_cached_spdx_ids = manager.dict()
        thread_cached_license_info = manager.dict()
        thread_lock = manager.Lock()

        num_cpus = os.cpu_count()
        processes = list()
        i = 0

        if not scan_dir:
            return

        if not os.path.exists(self._non_cached_scan_dir):
            os.makedirs(self._non_cached_scan_dir)

        while i < num_cpus:
            f_list = list()
            file_lists.append(f_list)
            i += 1

        i = 0
        for root, dirs, files in os.walk(scan_dir):
            for file in files:
                if i >= num_cpus:
                    i = 0
                file_path = os.path.join(root, file)
                if os.path.basename(file_path) not in git_files and os.path.isfile(
                    file_path
                ):
                    file_lists[i].append(file_path)
                i += 1

        for f_list in file_lists:
            p = multiprocessing.Process(
                target=self._db_cache_clear_job,
                args=(
                    manager,
                    f_list,
                    thread_cached_spdx_ids,
                    thread_cached_license_info,
                    thread_lock,
                ),
            )
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        # convert dict to set
        for spdx_id in thread_cached_spdx_ids:
            # ignore blank cases
            if spdx_id:
                self.cached_spdx_ids.add(spdx_id)

        # convert to regular dict instead of manager.dict()
        for spdx_id in thread_cached_license_info:
            for file in thread_cached_license_info[spdx_id]:
                if spdx_id not in self.cached_licenses_info:
                    self.cached_licenses_info[spdx_id] = []

                self.cached_licenses_info[spdx_id].append(file)

        return self._non_cached_scan_dir

    # Dump cached scan results to cached.yaml, at the same location as
    # yaml_output_dir
    def report_cache_results(self, yaml_output_dir=None):
        if not yaml_output_dir or not self.cached_licenses_info:
            return

        cached_yaml_path = f"{yaml_output_dir}/{common.cached_yaml_fn}"

        with open(cached_yaml_path, "w") as cached_info_f:
            yaml.dump(self.cached_licenses_info, cached_info_f)

        print(f"Results from cache documented at: {cached_yaml_path}")
