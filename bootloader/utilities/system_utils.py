import platform

import botocore.exceptions as bce
import flexsea.utilities as fxu

from bootloader.exceptions import exceptions
import bootloader.utilities.config as cfg


# ============================================
#                  check_os
# ============================================
def check_os() -> None:
    """
    Makes sure we're running on a supported OS.

    Raises
    ------
    RuntimeError
        If the detected operating system is not supported.
    """
    currentOS = platform.system().lower()
    try:
        assert currentOS in cfg.supportedOS
    except AssertionError as err:
        msg = f"Detected: `{currentOS}`, which is an unsupported OS. Supported OS:\n"
        for _os in cfg.supportedOS:
            msg += f"\t* {_os}\n"
        raise RuntimeError(msg) from err


# ============================================
#                 setup_cache
# ============================================
def setup_cache() -> None:
    """
    Creates the directories where the firmware files, bootloader tools,
    and pre-compiled C libraries are downloaded and installed to.
    """
    cfg.firmwareDir.mkdir(parents=True, exist_ok=True)
    cfg.toolsDir.mkdir(parents=True, exist_ok=True)


# ============================================
#                 check_tools
# ============================================
def check_tools(target: str) -> None:
    """
    The bootloader requires tools from PSoC and STM in order to
    flash the microcontrollers. Here we make sure that those tools
    are installed. If they aren't, then we download and install
    them.

    Tool directories are zip archives.

    Raises
    ------
    botocore.exceptions.EndpointConnectionError
        If we cannot connect to AWS.

    S3DownloadError
        If a tool fails to download.
    """
    _os = platform.system().lower()
    _bootloaderTools = cfg.bootloaderTools[_os][target]

    for tool in _bootloaderTools:
        dest = cfg.toolsDir.joinpath(tool)

        if not dest.exists():
            try:
                # boto3 requires dest be either IOBase or str
                toolObj = str(Path(_os).joinpath(tool).as_posix())
                fxu.download(toolObj, cfg.toolsBucket, str(dest), cfg.dephyProfile)
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
