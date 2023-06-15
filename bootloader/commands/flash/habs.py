from pathlib import Path
import sys
from time import sleep

from cleo.helpers import argument
from flexsea.utilities.aws import s3_download
import flexsea.utilities.constants as fxc
from semantic_version import Version

import bootloader.utilities.constants as bc
from bootloader.utilities.system_utils import call_flash_tool

from .base_flash import BaseFlashCommand


# ============================================
#              FlashHabsCommand
# ============================================
class FlashHabsCommand(BaseFlashCommand):
    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self.name = "flash habs"
        self.description = "Flashes new firmware onto Habsolute."
        self.help = self._help()

        self.arguments.append(
            argument("to", "Version to flash, e.g., `9.1.0`, or path to file to use.")
        )

        self._to: str = ""

        self.hidden = False

    # -----
    # _parse_options
    # -----
    def _parse_options(self) -> None:
        super()._parse_options()

        self._to = self.argument("to")
        self._target = "habs"

    # -----
    # _get_firmware_file
    # -----
    def _get_firmware_file(self) -> None:
        # If self._to is a file instead of a version string,
        # validate_given_firmware_version raises a ValueError
        try:
            desiredFirmwareVersion = validate_given_firmware_version(
                self._to, not self.option("no-interaction")
            )
        except ValueError:
            self._handle_firmware_file()
        else:
            self._handle_firmware_version(desiredFirmwareVersion)

    # -----
    # _handle_firmware_file
    # -----
    def _handle_firmware_file(self) -> None:
        self._fwFile = Path(self._to).expanduser().resolve()
        if not self._fwFile.is_file():
            raise RuntimeError(f"Error: could not find given firmware file: {self._to}")

    # -----
    # _handle_firmware_version
    # -----
    def _handle_firmware_version(self, desiredFirmwareVersion: Version) -> None:
        fName = f"{self._target}_version-{desiredFirmwareVersion}.hex"

        self._fwFile = fxc.dephyPath.joinpath(bc.firmwareDir, fName)

        if not fwFile.is_file():
            s3_download(fName, bc.dephyFirmwareBucket, self._fwFile, bc.dephyAwsProfile)

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        cmd = Path.joinpath(
            bc.toolsPath,
            "stm32_flash_loader",
            "stm32_flash_loader",
            "STMFlashLoader.exe",
        )
        portNum = re.search(r"\d+$", self._port).group(0)

        self._flashCmd = [
            f"{cmd}",
            "-c",
            "--pn",
            f"{portNum}",
            "--br",
            "115200",
            "--db",
            "8",
            "--pr",
            "NONE",
            "-i",
            "STM32F3_7x_8x_256K",
            "-e",
            "--all",
            "-d",
            "--fn",
            f"{self._fwFile}",
            "-o",
            "--set",
            "--vals",
            "--User",
            "0xF00F",
        ]

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        self._device.close()
        sleep(6)
        call_flash_tool(self._flashCmd)
        sleep(20)

    # -----
    # _confirm
    # -----
    def _confirm(self) -> None:
        self.line("<info>Summary</>:")
        self.line(f"\t* Flashing target: {self._target}")
        self.line(f"\t* To: {self._to}")
        msg = "\t* Using Mn firmware version for communication with target: "
        msg += f"{self._currentMnFw}"
        self.line(msg)

        if not self.option("no-interaction"):
            if not self.confirm("Proceed?"):
                self.line("<error>Aborting.</>")
                sys.exit(1)

    # -----
    # _help
    # -----
    def _help(self) -> str:
        return "Flashes new firmware onto Habsolute."
