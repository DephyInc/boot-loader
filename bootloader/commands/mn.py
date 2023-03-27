from pathlib import Path
from time import sleep

import bootloader.utilities.config as cfg
from bootloader.utilities.system_utils import call_flash_tool

from .flash_mcu import FlashMcuCommand


# ============================================
#            FlashManageCommand
# ============================================
class FlashManageCommand(FlashMcuCommand):
    """
    Flashes new firmware onto Manage (Mn).
    """

    name = "mn"

    description = "Flashes new firmware onto Manage (Mn)."

    help = """
    Flashes new firmware onto Mn. Requires the version of the firmware currently
    on Mn as well as the desired firmware version/file.

    NOTE: If the bootloading process fails or is interrupted, the device will
    most likely be bricked and must therefore be flashed manually using a STM
    programmer.

    # Examples
    ----------
    # Bootload from 7.2.0 to 9.1.0
    > bootload mn 7.2.0 9.1.0

    # Instead of a desired firmware version, you can pass a dfu file
    > bootload mn 9.1.0 /path/to/dfu/file.dfu
    """

    # -----
    # _get_target
    # -----
    def _get_target(self) -> None:
        self._target = "mn"

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        self._flashCmd = [
            f"{Path(cfg.toolsDir).joinpath('DfuSeCommand.exe')}",
            "-c",
            "-d",
            "--fn",
            f"{self._fwFile}",
        ]

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        self._device.close()
        del self._device
        sleep(3)
        sleep(10)
        call_flash_tool(self._flashCmd)
