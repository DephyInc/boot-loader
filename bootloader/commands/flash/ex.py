from time import sleep

from cleo.helpers import argument
from semantic_version import Version

from bootloader.utilities.help import ex_help
from bootloader.utilities.system_utils import call_flash_tool
from bootloader.utilities.system_utils import get_fw_file
from bootloader.utilities.system_utils import psoc_flash_command

from .base_flash import BaseFlashCommand


# ============================================
#              FlashExCommand
# ============================================
class FlashExCommand(BaseFlashCommand):
    name = "flash ex"
    description = "Flashes new firmware onto Execute."
    help = ex_help()
    hidden = False

    arguments = [
        argument("port", "Port the device is on, e.g., `COM3`."),
        argument("currentMnFw", "Manage's current firmware, e.g., `7.2.0`."),
        argument("to", "Version to flash, e.g., `9.1.0`, or path to file to use."),
        argument("rigidVersion", "PCB hardware version, e.g., `4.1B`."),
        argument("motorType", "Either 'actpack', 'exo', or '6:1-9:1'"),
        # argument("i2t", "i2t preset letter. Default is B before 10 and D after."),
    ]

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        # The mn and ex filenames don't have B in them for rigid 4.1B, since
        # they're the same file for rigid 4.1 and 4.1B. In order to avoid having
        # duplicate files with different names on S3, we just handle it here
        if self._rigidVersion.endswith("B") or self._rigidVersion.endswith("b"):
            self._rigidVersion = self.rigidVersion.lower()
            self._rigidVersion = self._rigidVersion.rstrip("b")

        # Additionally, ex filenames don't differentiate between 4.1 and 4.0,
        # so for the same reasons as above, there is only a 4.0 file, so we
        # convert it here
        if self._rigidVersion == "4.1":
            self._rigidVersion = "4.0"

        self._target = "ex"

    # -----
    # _handle_firmware_version
    # -----
    def _handle_firmware_version(self, version: Version) -> None:
        fName = f"{self._target}_version-{version}_"
        fName += f"rigid-{self._rigidVersion}_motor-{self._motorType}.cyacd"
        # fName += f"rigid-{self._rigidVersion}_motor-{self._motorType}_"
        # fName += f"i2t-{self._i2t}.cyacd"

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
        sleep(2)
        self._device.close()
        sleep(2)
        call_flash_tool(self._flashCmd)
        sleep(20)
