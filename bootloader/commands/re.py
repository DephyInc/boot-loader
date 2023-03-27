from pathlib import Path
from time import sleep

import bootloader.utilities.config as cfg
from bootloader.utilities.system_utils import call_flash_tool

from .flash_mcu import FlashMcuCommand


# ============================================
#            FlashRegulateCommand
# ============================================
class FlashRegulateCommand(FlashMcuCommand):
    """
    Flashes new firmware onto Regulate (Re).
    """

    name = "re"

    description = "Flashes new firmware onto Regulate (Re)."

    help = """
    Flashes new firmware onto Re. Requires the version of the firmware currently
    on Mn as well as the desired firmware version/file for Re.

    NOTE: If the bootloading process fails or is interrupted, the device will
    most likely be bricked and must therefore be flashed manually using a PSoC
    programmer.

    # Examples
    ----------
    # Bootload to 9.1.0 when Mn has 7.2.0 on it
    > bootload mn 7.2.0 9.1.0

    # Instead of a desired firmware version, you can pass a cyacd file
    > bootload re 7.2.0 /path/to/dfu/file.cyacd
    """

    # -----
    # _get_target
    # -----
    def _get_target(self) -> None:
        self._target = "re"

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        self._flashCmd = [
            f"{Path.joinpath(cfg.toolsDir, 'psocbootloaderhost.exe')}",
            f"{self._port}",
            f"{self._fwFile}",
        ]

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        sleep(3)
        self._device.close()
        call_flash_tool(self._flashCmd)
