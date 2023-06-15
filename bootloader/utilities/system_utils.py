import subprocess as sub
from typing import List

import bootloader.utilities.constants as bc


# ============================================
#                setup_cache
# ============================================
def setup_cache() -> None:
    bc.firmwarePath.mkdir(parents=True, exist_ok=True)
    bc.toolsPath.mkdir(parents=True, exist_ok=True)


# ============================================
#             call_flash_tool
# ============================================
def call_flash_tool(cmd: List[str]) -> None:
    """
    Attempts to call the flash command `cmd`. If the call fails, we
    try again until the max attempts have been reached.
    """
    # This is done to prevent unboundlocalerror, which happens if
    # a calledprocesserror is raised if the process never successfully
    # completes
    proc = None

    for _ in range(5):
        try:
            proc = sub.run(cmd, capture_output=False, check=True, timeout=360)
        except sub.CalledProcessError:
            continue
        except sub.TimeoutExpired as err:
            raise sub.TimeoutExpired(cmd, 360) from err
        if proc.returncode == 0:
            break
    if proc is None or proc.returncode != 0:
        raise RuntimeError("Error: flash command failed.")
