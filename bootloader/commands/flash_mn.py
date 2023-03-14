from pathlib import Path
from time import sleep
from typing import List

from cleo.helpers import option

import bootloader.utilities.config as cfg

from .flash_mcu import FlashMcuCommand


# ============================================
#             FlashManageCommand
# ============================================
class FlashManageCommand(FlashMcuCommand):
    """
    Flashes new firmware onto Manage.
    """

    name = "mn"

    description = "Flashes new firmwware onto Manage."

    help = """
    Flashes new firmware onto Manage.

    Examples
    --------
    # Arguments are the current manage firmware version and desired firmware version
    > bootload mn 7.2.0 9.1.0

    # Can also pass a file as the desired firmware. The path can be relative
    > bootload mn 9.1.0 /path/to/firmware_file

    # If the device doesn't know it's own meta-info (side, rigid version, etc.),
    # you can specify those with options. Also useful for flashing firmware from
    # one type of device onto another, e.g., actpack firmware onto an exo
    > bootload mn 7.2.0 10.1.2 -d actpack -r 4.1B

    # The `lib` option can be used to specify the C library to use. The path can
    # be relative
    > bootload mn 7.2.0 9.1.0 -l /path/to/pre_compiled_c_library_file
    """

    _target: str = "mn"

    # -----
    # __new__
    # -----
    def __new__(cls):
        obj = super().__new__(cls)
        obj.options.append(option("side", "-s", "Left or right.", flag=False))
        return obj

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        self._device.close()
        del self._device
        sleep(3)
        sleep(10)
        self._call_flash_tool()

    # -----
    # _flashCmd
    # -----
    @property
    def _flashCmd(self) -> List[str]:
        flashCmd = [
            f"{Path(cfg.toolsDir).joinpath('DfuSeCommand.exe')}",
            "-c",
            "-d",
            "--fn",
            f"{self._fwFile}",
        ]

        return flashCmd
