import os
from pathlib import Path
import subprocess as sub
from typing import List
import zipfile

import botocore.exceptions as bce
from flexsea.utilities.aws import s3_download
from flexsea.utilities.constants import dephyPublicFilesBucket

import bootloader.utilities.config as cfg


# ============================================
#               get_flash_tools
# ============================================
def get_flash_tools(target: str, operatingSystem: str) -> None:
    """
    Checks to make sure that the tools required to flash the desired
    target on the current OS are present. If they aren't, then we
    try to download them from S3.
    """
    _bootloaderTools = cfg.bootloaderTools[operatingSystem][target]

    for tool in _bootloaderTools:
        dest = cfg.toolsPath.joinpath(tool)

        if not dest.exists():
            try:
                # boto3 requires dest be either IOBase or str
                obj = str(Path(cfg.toolsDir).joinpath(operatingSystem, tool).as_posix())
                s3_download(obj, dephyPublicFilesBucket, str(dest), None)
            except bce.EndpointConnectionError as err:
                raise err
            except AssertionError as err:
                raise RuntimeError(f"Error: checksums don't equal: `{tool}`") from err

            if zipfile.is_zipfile(dest):
                with zipfile.ZipFile(dest, "r") as archive:
                    base = dest.name.split(".")[0]
                    extractedDest = Path(os.path.dirname(dest)).joinpath(base)
                    archive.extractall(extractedDest)


# ============================================
#             call_flash_tool
# ============================================
def call_flash_tool(cmd: List[str]) -> None:
    """
    Attempts to call the flash command `cmd`. If the call fails, we
    try again until the max attempts have been reached.
    """
    for _ in range(5):
        try:
            proc = sub.run(cmd, capture_output=False, check=True, timeout=360)
        except sub.CalledProcessError:
            continue
        except sub.TimeoutExpired as err:
            raise sub.TimeoutExpired(cmd, 360) from err
        if proc.returncode == 0:
            break
    if proc.returncode != 0:
        raise RuntimeError("Error: flash command failed.")


# ============================================
#                setup_cache
# ============================================
def setup_cache() -> None:
    cfg.firmwarePath.mkdir(parents=True, exist_ok=True)
    cfg.toolsPath.mkdir(parents=True, exist_ok=True)
