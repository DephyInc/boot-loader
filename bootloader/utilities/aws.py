import os
from pathlib import Path
from typing import List
import zipfile

import boto3
from botocore.client import BaseClient
import botocore.exceptions as bce
from flexsea.utilities import download

from bootloader.exceptions import exceptions
from bootloader.utilities import config as cfg


# ============================================
#             get_s3_object_info
# ============================================
def get_s3_object_info(bucket: str) -> List[str] | dict:
    session = boto3.Session(profile_name=cfg.dephyProfile)
    client = session.client("s3")
    # The firmware and C libraries are in different buckets. The devices
    # and hardware can be obtained from the firmware bucket
    objs = get_s3_objects(bucket, client)
    client.close()

    if bucket == cfg.firmwareBucket:
        return _parse_firmware_objects(objs)
    if bucket == cfg.libsBucket:
        return _parse_lib_objects(objs)
    raise ValueError("Unrecognized bucket.")


# ============================================
#                get_s3_objects
# ============================================
def get_s3_objects(bucket: str, client: BaseClient, prefix: str = "") -> List:
    """
    Recursively loops over all directories in a bucket and returns a
    list of files.

    Parameters
    ----------
    bucket : str
        The name of the bucket we're getting files from.

    client : botocore.client.BaseClient
        The object providing an interface to S3.

    prefix : str
        The directory we're looping over. If `""`, then we get the
        top-level directories.

    Returns
    -------
    List[str]
        A list of all the objects in the bucket.
    """
    objectList = []
    objects = client.list_objects_v2(Bucket=bucket, Delimiter="/", Prefix=prefix)

    if "CommonPrefixes" in objects:
        for pre in objects["CommonPrefixes"]:
            objectList += get_s3_objects(bucket, client, pre["Prefix"])

    if "Contents" in objects:
        return objectList + [obj["Key"] for obj in objects["Contents"][1:]]
    return objectList


# ============================================
#           _parse_firmware_objects
# ============================================
def _parse_firmware_objects(objects: List[str]) -> dict:
    """
    Converts the list of full-path firmware file names into a
    dictionary for easier display.

    Parameters
    ----------
    objects : List[str]
        List of full paths for firmware files from S3.

    Returns
    -------
    info : dict
        `objects` converted to a hierarchial dictionary form for
        cleaner display.
    """
    info = {}

    for obj in objects:
        version, device, hardware, _ = obj.split("/")
        if version not in info:
            info[version] = {
                hardware: set(
                    [
                        device,
                    ]
                )
            }
        else:
            if hardware not in info[version]:
                info[version][hardware] = set(
                    [
                        device,
                    ]
                )
            else:
                info[version][hardware].add(device)
    return info


# ============================================
#              _parse_lib_objects
# ============================================
def _parse_lib_objects(objects: List[str]) -> List[str]:
    libs = set()

    for obj in objects:
        lib = obj.split("/")[1]
        libs.add(lib)

    return sorted(list(libs))


# ============================================
#               get_remote_file
# ============================================
def get_remote_file(fName: str, bucket: str, dest: str) -> None:
    """
    Searches the given aws bucket for the given file and downloads it to
    `dest`.
    """
    fPath = Path(fName)
    # https://tinyurl.com/4scnuk6c
    session = boto3.Session(profile_name=cfg.dephyProfile)
    client = session.client("s3")
    paginator = client.get_paginator("list_objects_v2")
    pageIterator = paginator.paginate(Bucket=bucket)
    objects = pageIterator.search(f"Contents[?contains(Key, `{fPath.name}`)][]")
    items = [item["Key"] for item in objects]
    # There should only be one match. If not, we don't know which one to go with
    try:
        assert len(items) == 1
    except AssertionError as err:
        raise FileNotFoundError from err
    download(items[0], bucket, dest, cfg.dephyProfile)


# ============================================
#               get_flash_tools
# ============================================
def get_flash_tools(target: str, _os: str) -> None:
    """
    Checks to see if the tools required for flashing `target` are already
    downloaded. If they aren't, then we download them.
    """
    for tool in cfg.bootloaderTools[_os][target]:
        dest = cfg.toolsDir.joinpath(tool)

        if not dest.exists():
            try:
                # boto3 requires dest be either IOBase or str
                toolObj = str(Path(_os).joinpath(tool).as_posix())
                download(toolObj, cfg.toolsBucket, str(dest), cfg.dephyProfile)
            except bce.EndpointConnectionError as err:
                raise err
            except AssertionError as err:
                raise exceptions.S3DownloadError(
                    cfg.toolsBucket, toolObj, str(dest)
                ) from err

            if zipfile.is_zipfile(dest):
                with zipfile.ZipFile(dest, "r") as archive:
                    base = dest.name.split(".")[0]
                    extractedDest = Path(os.path.dirname(dest)).joinpath(base)
                    archive.extractall(extractedDest)
