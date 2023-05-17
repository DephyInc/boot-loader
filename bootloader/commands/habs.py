from pathlib import Path
import re
from time import sleep

import semantic_version as sem

import bootloader.utilities.config as cfg
from bootloader.utilities.system_utils import call_flash_tool

from .flash_mcu import FlashMcuCommand


# ============================================
#            FlashHabsoluteCommand
# ============================================
class FlashHabsoluteCommand(FlashMcuCommand):
    """
    Flashes new firmware onto Habsolute (Habs).
    """

    name = "habs"

    description = "Flashes new firmware onto Habsolute (Habs)."

    help = """
    Flashes new firmware onto Habs. Requires the version of the firmware currently
    on Mn as well as the desired firmware version/file for Habs.

    NOTE: Habs has a special block of memory for bootloading, so if the bootloading
    process fails or is interrupted, it does not need to be flashed manually, you
    can simply re-run the command.

    NOTE: Bootloading habs currently requires Mn to be at 7.2.0.

    # Examples
    ----------
    # Bootload to 9.1.0 when Mn has 7.2.0 on it
    > bootload habs 7.2.0 9.1.0

    # Instead of a desired firmware version, you can pass a hex file
    > bootload habs 7.2.0 /path/to/dfu/file.hex
    """

    # -----
    # _get_target
    # -----
    def _get_target(self) -> None:
        self._target = "habs"

        if sem.Version(self._currentMnFw) != sem.Version("7.2.0"):
            raise RuntimeError("Error: Mn must be at 7.2.0 to flash Habs.")

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        cmd = Path.joinpath(
            cfg.toolsPath,
            "stm32_flash_loader",
            "stm32_flash_loader",
            "STMFlashLoader.exe",
        )
        portNum = re.search(r"\d+$", self._port).group(0)

        self._flashCmd = [
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

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        self._device.close()
        sleep(6)
        call_flash_tool(self._flashCmd)
        sleep(20)
