from pathlib import Path
import re
from time import sleep

from semantic_version import Version

import bootloader.utilities.constants as bc
from bootloader.utilities.system_utils import call_flash_tool
from bootloader.utilities.system_utils import get_fw_file

from .mcu import FlashMcuCommand


# ============================================
#              FlashHabsCommand
# ============================================
class FlashHabsCommand(FlashMcuCommand):
    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self.name = "flash habs"
        self.description = "Flashes new firmware onto Habsolute."
        self.help = self._help()

        self.hidden = False

    # -----
    # _parse_options
    # -----
    def _parse_options(self) -> None:
        super()._parse_options()

        self._target = "habs"

    # -----
    # _handle_firmware_version
    # -----
    def _handle_firmware_version(self, desiredFirmwareVersion: Version) -> None:
        fName = f"{self._target}_version-{desiredFirmwareVersion}.hex"
        self._fwFile = get_fw_file(fName)

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
    # _help
    # -----
    def _help(self) -> str:
        return "Flashes new firmware onto Habsolute."
