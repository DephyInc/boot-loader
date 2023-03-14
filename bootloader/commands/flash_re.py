from pathlib import Path
from time import sleep
from typing import List

import bootloader.utilities.config as cfg

from .flash_mcu import FlashMcuCommand


# ============================================
#             FlashRegulateCommand
# ============================================
class FlashRegulateCommand(FlashMcuCommand):
    """
    Flashes new firmware onto Regulate.
    """

    name = "re"

    description = "Flashes new firmwware onto Regulate."

    help = """
    Flashes new firmware onto Regulate.

    Examples
    --------
    # Arguments are the current manage firmware version and desired firmware version
    > bootload re 7.2.0 9.1.0

    # Can also pass a file as the desired firmware. The path can be relative
    > bootload re 9.1.0 /path/to/firmware_file

    # If the device doesn't know it's own meta-info (side, rigid version, etc.),
    # you can specify those with options. Also useful for flashing firmware from
    # one type of device onto another, e.g., actpack firmware onto an exo
    > bootload re 7.2.0 10.1.2 -d actpack -r 4.1B

    # The `lib` option can be used to specify the C library to use. The path can
    # be relative
    > bootload re 7.2.0 9.1.0 -l /path/to/pre_compiled_c_library_file
    """

    _target: str = "re"

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        sleep(3)
        self._device.close()
        self._call_flash_tool()

    # -----
    # _flashCmd
    # -----
    @property
    def _flashCmd(self) -> List[str]:
        flashCmd = [
            f"{Path.joinpath(cfg.toolsDir, 'psocbootloaderhost.exe')}",
            f"{self._device.port}",
            f"{self._fwFile}",
        ]

        return flashCmd
