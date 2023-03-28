import os
from time import sleep

from cleo.helpers import argument
from cleo.helpers import option

import bootloader.utilities.config as cfg
from bootloader.utilities.system_utils import call_flash_tool

from .base_flash_command import BaseFlashCommand


# ============================================
#            FlashXbeeCommand
# ============================================
class FlashXbeeCommand(BaseFlashCommand):
    """
    Sets up the xbee radio for inter-device communication.
    """

    name = "xbee"

    description = "Sets up the xbee radio for inter-device communication."

    arguments = [
        argument("currentMnFw", "Current firmware version on Manage, e.g., `7.2.0`."),
        argument("buddyAddress", "Address of device's buddy."),
    ]

    options = [
        option("address", "-a", "BT address. Default is the device id.", flag=False),
        option("baudRate", "-b", "Device baud rate.", flag=False, default=230400),
        option("libFile", "-l", "C lib for interacting with Manage.", flag=False),
        option("port", "-p", "Port the device is on, e.g., `COM3`.", flag=False),
        option("theme", None, "classic, light, dark, or none", flag=False),
    ]

    help = ""

    # -----
    # _parse_options
    # -----
    def _parse_options(self) -> None:
        self._currentMnFw = self.argument("currentMnFw")
        self._buddyAddress = self.argument("buddyAddress")

        self._address = self.option("address")
        self._baudRate = self.option("baudRate")
        self._libFile = self.option("libFile")
        self._port = self.option("port")
        self._theme = self.option("theme")

    # -----
    # _get_target
    # -----
    def _get_target(self) -> None:
        self._target = "xbee"

    # -----
    # _get_firmware_file
    # -----
    def _get_firmware_file(self) -> None:
        # Flashing xbee doesn't require a firmware file
        pass

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        if "windows" in self._os:
            pythonCmd = "python"
        else:
            pythonCmd = "python3"

        address = self._address if self._address else self._device.deviceId

        self._flashCmd = [
            pythonCmd,
            os.path.join(cfg.toolsDir, "xb24c.py"),
            self._port,
            address,
            self._buddyAddress,
            "upgrade",
        ]

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        self._device.close()
        sleep(3)
        call_flash_tool(self._flashCmd)
        sleep(20)
