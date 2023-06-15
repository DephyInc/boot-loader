import os

from cleo.helpers import argument
from bootloader.commands.flash.radio import FlashRadioCommand

import bootloader.utilities.constants as bc

from .radio import FlashRadioCommand


# ============================================
#              FlashXbeeCommand
# ============================================
class FlashXbeeCommand(FlashRadioCommand):
    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self.name = "flash xbee"
        self.description = "Flashes new firmware onto xbee."
        self.help = self._help()

        self.arguments.append(
            argument("buddyAddress", "Bluetooth address of device's pair.")
        )

        self._buddyAddress: str = ""

        self.hidden = False

    # -----
    # _parse_options
    # -----
    def _parse_options(self) -> None:
        super()._parse_options()

        self._buddyAddress = self.argument("buddyAddress")
        self._target = "xbee"

    # -----
    # _get_firmware_file
    # -----
    def _get_firmware_file(self) -> None:
        """
        Uses the bluetooth tools repo to create a bluetooth image file
        with the correct address.
        """
        # A firmware file isn't required for xbee

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        if "windows" in self.application._os:
            pythonCmd = "python"
        else:
            pythonCmd = "python3"

        address = self._address if self._address else self._device.id

        self._flashCmd = [
            pythonCmd,
            os.path.join(bc.toolsPath, "xb24c.py"),
            self._port,
            address,
            self._buddyAddress,
            "upgrade",
        ]

    # -----
    # _confirm
    # -----
    def _confirm(self) -> None:
        self.line("<info>Summary</>:")
        self.line(f"\t* Setting buddy bluetooth address as: {self._buddyAddress}")
        super()._confirm()

    # -----
    # _help
    # -----
    def _help(self) -> str:
        return "Flashes new firmware onto xbee."
