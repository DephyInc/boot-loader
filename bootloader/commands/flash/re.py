from time import sleep

from cleo.helpers import argument
from semantic_version import Version

from bootloader.utilities.system_utils import call_flash_tool
from bootloader.utilities.system_utils import get_fw_file
from bootloader.utilities.system_utils import psoc_flash_command

from .mcu import FlashMcuCommand


# ============================================
#              FlashReCommand
# ============================================
class FlashReCommand(FlashMcuCommand):
    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self.name = "flash re"
        self.description = "Flashes new firmware onto Regulate."
        self.help = self._help()
        self.hidden = False

        self.arguments.append(argument("led", "Either 'mono', 'multi', or 'stealth'"))

        self._led: str = ""

    # -----
    # _parse_options
    # -----
    def _parse_options(self) -> None:
        super()._parse_options()
        self._led = self.argument("led")
        self._target = "re"

    # -----
    # _handle_firmware_version
    # -----
    def _handle_firmware_version(self, desiredFirmwareVersion: Version) -> None:
        fName = f"{self._target}_version-{desiredFirmwareVersion}_"
        fName += f"rigid-{self._rigidVersion}_led-{self._led}color.cyacd"

        self._fwFile = get_fw_file(fName)

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        self._flashCmd = psoc_flash_command(self._port, self._fwFile)

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        sleep(3)
        self._device.close()
        call_flash_tool(self._flashCmd)

    # -----
    # _confirm
    # -----
    def _confirm(self) -> None:
        self.line("<info>Summary</>:")
        self.line(f"\t* LED pattern being used: {self._led}")
        super()._confirm()

    # -----
    # _help
    # -----
    def _help(self) -> str:
        return "Flashes new firmware onto Regulate."
