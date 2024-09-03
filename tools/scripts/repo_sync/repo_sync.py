#!/usr/bin/env python3
import os
import requests
import sqlite3
import shutil
import sys
import time
import hashlib
import logging
import logging.handlers
import bz2
import gzip
import datetime
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_path = "packages.vmware.com/photon/"
base_url = "https://packages.vmware.com/photon/"

# Request timeout in seconds
timeout = 10

# Number of retries for each request
file_max_retries = 5
folder_max_retries = 2
checksum_max_retries = 2

def info(message):
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:INFO: {message}")

def warning(message):
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:WARN: {message}")

def error(message):
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:ERROR: {message}")

def debug(message):
    #print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:DEBUG: {message}")
    pass

def should_include(href):
    """Check if the file should be included based on the given list."""
    include_extensions = [".gz", ".rpm", ".bz2", ".xml", ".xz"]
    for ext in include_extensions:
        if href.endswith(ext):
            return True
    return False


def detect_and_uncompress(file_path):
    """Detects the compression type of a file and uncompresses it."""
    func = None
    output_file = None

    if file_path.endswith(".gz"):
        output_file = file_path.rstrip(".gz")
        func = gzip.GzipFile
    elif file_path.endswith(".bz2"):
        output_file = file_path.rstrip(".bz2")
        func = bz2.BZ2File

    if not func:
        warn(f"detect_and_uncompress : Unsupported file type for {file_path}")
        return None

    if os.path.exists(output_file):
        os.remove(output_file)

    with func(file_path, "rb") as f_in:  # Changed to "rb" for reading in binary mode
        with open(output_file, "wb") as f_out:
            f_out.write(f_in.read())

    return output_file

def remove_unused_rpms(directory, rpms):
    for root, dirs, files in os.walk(directory):
        for file in files:
            # If the file is not in the rpms list, delete it
            if file not in rpms:
                file_path = os.path.join(root, file)
                os.remove(file_path)


def validate_repodata_checksums(repodata_folder):
    """Validate files inside the repodata directory using checksums from repomd.xml."""
    repomd_path = os.path.join(repodata_folder, "repomd.xml")
    if not os.path.exists(repomd_path):
        raise Exception(f"repomd.xml not found in {repodata_folder}")

    with open(repomd_path, "r") as file:
        repomd_content = file.read()

    primary_sqlite_filename = None
    soup = BeautifulSoup(repomd_content, "xml")
    for data in soup.find_all("data"):
        checksum = data.find("checksum").text
        file_path = os.path.join(repodata_folder, data.find("location").get("href"))

        if os.path.exists(file_path):
            computed_checksum = compute_checksum(file_path)
            if computed_checksum != checksum:
                raise Exception(
                    f"Checksum mismatch for {file_path}: expected {checksum}, got {computed_checksum}"
                )
        if "primary.sqlite" in file_path:
            primary_sqlite_filename = os.path.basename(file_path)

    if not primary_sqlite_filename:
        Exception(f"primary_sqlite file found in {repodata_folder}")

    return primary_sqlite_filename


def compute_checksum(file_path, algorithm="sha256"):
    """Compute the checksum of a file."""
    h = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def download_file(url, destination):
    """Download a file with retries and save it to the specified destination."""
    debug(f"Downloading file {url} to location {destination}")
    for i in range(file_max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            with open(destination, "wb") as file:
                file.write(response.content)
            return
        except requests.RequestException as e:
            warn(f"Error downloading {url}: {e}. Retrying in {2 ** i} seconds...")
            time.sleep(2**i)
    raise Exception(f"Failed to download {url} after {file_max_retries} retries.")


def download_files(url, destination_folder):
    """Download files from a URL and handle directory structure."""
    for i in range(folder_max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
        except requests.RequestException as e:
            if i < folder_max_retries - 1:
                warn(f"Retry {i + 1}/{folder_max_retries}: Error fetching {url}. Retrying...")
            else:
                warn(f"Error fetching {url}: {e}. Skipping this directory...")
                return

    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.find_all("a"):
        href = link.get("href")
        if not href or href == "../":
            continue

        path_parts = href.strip("/").split("/")
        if "x86_64" in path_parts or "noarch" in path_parts:
            continue

        full_url = urljoin(url, href)
        new_destination_folder = os.path.join(destination_folder, href.strip("/"))

        if href.endswith("/"):
            if "repodata" in href:
                # If the directory is repodata, remove it, download its contents and process it
                if os.path.exists(new_destination_folder):
                    shutil.rmtree(new_destination_folder)
                os.makedirs(new_destination_folder)

                download_files(full_url, new_destination_folder)
                primary_sqlite_filename = validate_repodata_checksums(
                    new_destination_folder
                )
                repo_name = url.rstrip('/').split('/')[-1]
                info(f"Syncing from {url} to {base_path}...")
                if "updates" in repo_name:
                    delete_files_not_in_repo_db(new_destination_folder, primary_sqlite_filename)
                download_rpms_from_sqlite(
                    new_destination_folder, url, primary_sqlite_filename
                )
                return  # Treat as leaf node, stop further recursion
            else:
                if not os.path.exists(new_destination_folder):
                    os.makedirs(new_destination_folder)
                download_files(full_url, new_destination_folder)
        else:
            if should_include(href):
                file_name = os.path.join(destination_folder, os.path.basename(href))
                download_file(full_url, file_name)

def delete_files_not_in_repo_db(repodata_folder, primary_sqlite_filename):
    """Delete RPMs updates repo based on the primary.sqlite.{bz2, gz} file."""
    sqlite_compressed_path = os.path.join(repodata_folder, primary_sqlite_filename)

    if not os.path.exists(sqlite_compressed_path):
        raise Exception(f"{sqlite_compressed_path} not found in {repodata_folder}")

    sqlite_path = detect_and_uncompress(sqlite_compressed_path)

    # Connect to the SQLite database
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()

    # Query to get all RPM filenames
    cursor.execute("SELECT location_href FROM packages")
    rpms = set(os.path.basename(row[0]) for row in cursor.fetchall())

    noarch_dir = os.path.join(repodata_folder, '..', 'noarch')
    noarch_dir = os.path.normpath(noarch_dir)
    remove_unused_rpms(noarch_dir, rpms)

    x86_64_dir = os.path.join(repodata_folder, '..', 'x86_64')
    x86_64_dir = os.path.normpath(x86_64_dir)
    remove_unused_rpms(x86_64_dir, rpms)

    # Close the database connection
    conn.close()
    os.remove(sqlite_path)

def download_rpms_from_sqlite(repodata_folder, url, primary_sqlite_filename):
    """Download RPMs based on the primary.sqlite.{bz2, gz} file."""
    sqlite_compressed_path = os.path.join(repodata_folder, primary_sqlite_filename)

    if not os.path.exists(sqlite_compressed_path):
        raise Exception(f"{sqlite_compressed_path} not found in {repodata_folder}")

    sqlite_path = detect_and_uncompress(sqlite_compressed_path)

    # Connect to the SQLite database
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()

    # Query to get all RPM paths
    cursor.execute("SELECT pkgId,location_href FROM packages")
    rpms = cursor.fetchall()

    for rpm in rpms:
        sha256 = rpm[0]
        rpm_path = rpm[1]
        rpm_url = urljoin(url, rpm_path)
        destination_folder = os.path.join(repodata_folder, "../")
        destination_folder = os.path.join(destination_folder, os.path.dirname(rpm_path))
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        file_name = os.path.join(destination_folder, os.path.basename(rpm_path))

        if os.path.exists(file_name):
            computed_checksum = compute_checksum(file_name)
            if computed_checksum != sha256:
                os.remove(file_name)
                warn(f"Checksum mismatch detected for {file_name}: expected {sha256}, but found {computed_checksum}. Re-downloading...")
            else:
                continue

        for i in range(checksum_max_retries):
            download_file(rpm_url, file_name)
            computed_checksum = compute_checksum(file_name)
            if computed_checksum != sha256:
                os.remove(file_name)
                if i < checksum_max_retries - 1:
                    warn(f"Retry {i + 1}/{checksum_max_retries}: Checksum mismatch for {file_name}: expected {sha256}, got {computed_checksum}, Downloading again...")
                else:
                    raise Exception(
                        f"Checksum mismatch for {file_name}: expected {sha256}, got {computed_checksum}"
                    )
    conn.close()
    os.remove(sqlite_path)


def read_config(file_path):
    """Read the list of relative paths from a configuration file."""
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        paths = [
            line.strip() for line in lines if line.strip() and not line.startswith("#")
        ]
        return paths
    except FileNotFoundError:
        error(f"{file_path} configuration file was not found.")
        return []
    except IOError as e:
        error(f"Error reading file {file_path}: {e}")
        return []
    except Exception as e:
        error(f"An unexpected error occurred: {e}")
        return []

usage_text = f"""
    A script to synchronize RPM repositories from {base_url} to local directory.
      - The script automatically reads input parameters from 'repo_sync.conf' in the current directory.
      - At present, no command-line arguments are accepted except --help or -h.

    Example:
      Simply run:
      ./repo_sync.py  # Uses 'repo_sync.conf' in current directory for input parameters
    """


parser = argparse.ArgumentParser(description=usage_text,formatter_class=argparse.RawTextHelpFormatter)
args = parser.parse_args()

try:
    config_file_path = "repo_sync.conf"
    relative_paths = read_config(config_file_path)

    for relative_path in relative_paths:
        full_url = urljoin(base_url, relative_path.lstrip("/"))
        destination_folder = os.path.join(base_path, relative_path.lstrip("/"))
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        download_files(full_url, destination_folder)
        info(f"Syncing of {full_url} repository completed successfully.\n")

except Exception as e:
    logging.error(e)
    sys.exit(1)
