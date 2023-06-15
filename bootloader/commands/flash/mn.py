from pathlib import Path
from time import sleep

from cleo.helpers import argument
import flexsea.utilities.constants as fxc
from flexsea.utilities.aws import s3_download
from semantic_version import Version

import bootloader.utilities.constants as bc
from bootloader.utilities.system_utils import call_flash_tool

from .mcu import FlashMcuCommand


# ============================================
#              FlashMnCommand
# ============================================
class FlashMnCommand(FlashMcuCommand):
    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self.name = "flash mn"
        self.description = "Flashes new firmware onto Manage."
        self.help = self._help()
        self.hidden = False

        self.arguments.append(argument("device", "Name of the device, e.g., actpack."))
        self.arguments.append(argument("side", "left, right, or none."))

        self._deviceName: str = ""
        self._side: str = ""

    # -----
    # _parse_options
    # -----
    def _parse_options(self) -> None:
        super()._parse_options()
        self._deviceName = self.argument("device")
        self._side = self.argument("side")
        self._target = "mn"

    # -----
    # _handle_firmware_version
    # -----
    def _handle_firmware_version(self, desiredFirmwareVersion: Version) -> None:
        fName = f"{self._target}_version-{desiredFirmwareVersion}_"
        fName += f"device-{self._deviceName}_rigid-{self._rigidVersion}_"
        fName += f"side-{self._side}.dfu"

        self._fwFile = fxc.dephyPath.joinpath(bc.firmwareDir, fName)

        if not self._fwFile.is_file():
            s3_download(fName, bc.dephyFirmwareBucket, self._fwFile, bc.dephyAwsProfile)

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        self._flashCmd = [
            f"{Path(bc.toolsPath).joinpath('DfuSeCommand.exe')}",
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

    # -----
    # _confirm
    # -----
    def _confirm(self) -> None:
        self.line("<info>Summary</>:")
        self.line(f"\t* Device being flashed: {self._deviceName}")
        self.line(f"\t* Side being flashed: {self._side}")
        super()._confirm()

    # -----
    # _help
    # -----
    def _help(self) -> str:
        return "Flashes new firmware onto Manage."
