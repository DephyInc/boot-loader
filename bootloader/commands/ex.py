from pathlib import Path
from time import sleep

import bootloader.utilities.config as cfg
from bootloader.utilities.system_utils import call_flash_tool

from .flash_mcu import FlashMcuCommand


# ============================================
#            FlashExecuteCommand
# ============================================
class FlashExecuteCommand(FlashMcuCommand):
    """
    Flashes new firmware onto Execute (Ex).
    """

    name = "ex"

    description = "Flashes new firmware onto Execute (Ex)."

    help = """
    Flashes new firmware onto Ex. Requires the version of the firmware currently
    on Mn as well as the desired firmware version/file for Ex.

    NOTE: If the bootloading process fails or is interrupted, the device will
    most likely be bricked and must therefore be flashed manually using a PSoC
    programmer.

    # Examples
    ----------
    # Bootload to 9.1.0 when Mn has 7.2.0 on it
    > bootload ex 7.2.0 9.1.0

    # Instead of a desired firmware version, you can pass a cyacd file
    > bootload ex 7.2.0 /path/to/dfu/file.cyacd
    """

    # -----
    # _get_target
    # -----
    def _get_target(self) -> None:
        self._target = "ex"

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        self._flashCmd = [
            f"{Path.joinpath(cfg.toolsPath, 'psocbootloaderhost.exe')}",
            f"{self._port}",
            f"{self._fwFile}",
        ]

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        sleep(2)
        self._device.close()
        sleep(2)
        call_flash_tool(self._flashCmd)
        sleep(20)
