from pathlib import Path
import re
from time import sleep
from typing import List

import bootloader.utilities.config as cfg

from .flash_mcu import FlashMcuCommand


# ============================================
#             FlashHabsoluteCommand
# ============================================
class FlashHabsoluteCommand(FlashMcuCommand):
    """
    Flashes new firmware onto Habsolute.
    """

    name = "habs"

    description = "Flashes new firmwware onto Habsolute."

    help = """
    Flashes new firmware onto Habsolute.

    Examples
    --------
    # Arguments are the current manage firmware version and desired firmware version
    > bootload habs 7.2.0 9.1.0

    # Can also pass a file as the desired firmware. The path can be relative
    > bootload habs 9.1.0 /path/to/firmware_file

    # If the device doesn't know it's own meta-info (side, rigid version, etc.),
    # you can specify those with options. Also useful for flashing firmware from
    # one type of device onto another, e.g., actpack firmware onto an exo
    > bootload habs 7.2.0 10.1.2 -d actpack -r 4.1B

    # The `lib` option can be used to specify the C library to use. The path can
    # be relative
    > bootload habs 7.2.0 9.1.0 -l /path/to/pre_compiled_c_library_file
    """

    _target: str = "habs"

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        self._device.close()
        sleep(6)
        self._call_flash_tool()
        sleep(20)

    # -----
    # _flashCmd
    # -----
    @property
    def _flashCmd(self) -> List[str]:
        cmd = Path.joinpath(
            cfg.toolsDir,
            "stm32_flash_loader",
            "stm32_flash_loader",
            "STMFlashLoader.exe",
        )
        portNum = re.search(r"\d+$", self._device.port).group(0)

        flashCmd = [
            f"{cmd}",
            "-c",
            "--pn",
            f"{portNum}",
            "--br",
            "115200",
            "--db",
            "8",
            "--pr",
            "NONE",
            "-i",
            "STM32F3_7x_8x_256K",
            "-e",
            "--all",
            "-d",
            "--fn",
            f"{self._fwFile}",
            "-o",
            "--set",
            "--vals",
            "--User",
            "0xF00F",
        ]

        return flashCmd
