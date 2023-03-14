import os
from time import sleep
from typing import List

from cleo.helpers import argument
from cleo.helpers import option

import bootloader.utilities.config as cfg

from .flash_mcu import FlashMcuCommand


# ============================================
#            FlashXbeeCommand
# ============================================
class FlashXbeeCommand(FlashMcuCommand):
    """
    Sets up the xbee radio for inter-device communication.
    """

    name = "xbee"

    description = "Sets up the xbee radio for inter-device communication."

    help = ""

    _address: str = ""
    _target: str = "xbee"

    # -----
    # __new__
    # -----
    def __new__(cls):
        obj = super().__new__(cls)
        _ = obj.arguments.pop()
        obj.arguments.append(argument("buddyAddress", "Address of device's buddy."))
        obj.options.append(option("address", "-a", "BT address.", flag=False))

        return obj

    # -----
    # _get_firmware_file
    # -----
    def _get_firmware_file(self) -> None:
        # Flashing xbee doesn't require a firmware file, so we take this
        # opportunity to set the address attribute
        if self.option("address"):
            self._address = self.option("address")
        else:
            self._address = self._device.deviceId

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        self._device.close()
        sleep(3)
        self._call_flash_tool()
        sleep(20)

    # -----
    # _flashCmd
    # -----
    @property
    def _flashCmd(self) -> List[str]:
        if self._os == "windows":
            pythonCmd = "python"
        else:
            pythonCmd = "python3"

        cmd = [
            pythonCmd,
            os.path.join(cfg.toolsDir, "xb24c.py"),
            self._device.port,
            self._address,
            self.argument("buddyAddress"),
            "upgrade",
        ]

        return cmd
