from pathlib import Path
from time import sleep

from cleo.helpers import argument
from flexsea.utilities.aws import s3_download
import flexsea.utilities.constants as fxc
from semantic_version import Version

import bootloader.utilities.constants as bc
from bootloader.utilities.system_utils import call_flash_tool

from .mcu import FlashMcuCommand


# ============================================
#              FlashExCommand
# ============================================
class FlashExCommand(FlashMcuCommand):
    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self.name = "flash ex"
        self.description = "Flashes new firmware onto Execute."
        self.help = self._help()
        self.hidden = False

        self.arguments.append(
            argument("motorType", "Either 'actpack', 'exo', or '6:1-9:1'")
        )
        self.arguments.append(
            argument("i2t", "i2t preset letter. Default is B before 10 and D after.")
        )

        self._motorType: str = ""
        self._i2t: str = ""

    # -----
    # _parse_options
    # -----
    def _parse_options(self) -> None:
        super()._parse_options()
        self._motorType = self.argument("motorType")

        if self._motorType == "exo":
            self._motorType = "dephy"
        elif self._motorType == "6:1-9:1":
            self._motorType = "6191"

        self._i2t = self.argument("i2t").upper()
        self._target = "ex"

    # -----
    # _handle_firmware_version
    # -----
    def _handle_firmware_version(self, desiredFirmwareVersion: Version) -> None:
        fName = f"{self._target}_version-{desiredFirmwareVersion}_"
        fName += f"rigid-{self._rigidVersion}_motor-{self._motorType}_"
        fName += f"i2t-{self._i2t}.cyacd"

        self._fwFile = fxc.dephyPath.joinpath(bc.firmwareDir, fName)

        if not self._fwFile.is_file():
            s3_download(
                fName, bc.dephyFirmwareBucket, str(self._fwFile), bc.dephyAwsProfile
            )

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        self._flashCmd = [
            f"{Path.joinpath(bc.toolsPath, 'psocbootloaderhost.exe')}",
            f"{self._port}",
            f"{self._fwFile}",
        ]

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        sleep(2)
        self._device.close()
        sleep(2)
        call_flash_tool(self._flashCmd)
        sleep(20)

    # -----
    # _confirm
    # -----
    def _confirm(self) -> None:
        self.line("<info>Summary</>:")
        self.line(f"\t* Motor being flashed: {self._motorType}")
        self.line(f"\t* i2t preset being flashed: {self._i2t}")
        super()._confirm()

    # -----
    # _help
    # -----
    def _help(self) -> str:
        return "Flashes new firmware onto Execute."
