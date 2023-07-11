from cleo.commands.command import Command as BaseCommand
from cleo.helpers import argument

import bootloader.utilities.constants as bc
from bootloader.utilities.help import flash_config_help


# ============================================
#             FlashConfigCommand
# ============================================
class FlashConfigCommand(BaseCommand):
    name = "flash config"
    description = "Flashes the files stored in the given config."
    help = flash_config_help()

    arguments = [
        argument("port", "Port the device is on, e.g., `COM3`."),
        argument("currentMnFw", "Manage's current firmware, e.g., `7.2.0`."),
        argument("configName", "Name of the configuration to use."),
    ]

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self._port: str = ""
        self._currentMnFw: str = ""
        self._configName: str = ""

    # -----
    # handle
    # -----
    def handle(self) -> int:
        self._port = self.argument("port")
        self._currentMnFw = self.argument("currentMnFw")
        self._configName = self.argument("configName")

        # Download and extract config
        self.call("download config", self._configName)
        # Read info file
        with open(
            bc.configsPath.joinpath(self._configName, bc.configInfoFile), "r"
        ) as fd:
            info = yaml.safe_load(fd)
        # For each target in the info file, flash with the corresponding file
        if "habs-file" in info:
            self.call(
                "flash habs", f"{self._port} {self._currentMnFw} {info['habs-file']}"
            )
        # For re, ex, and mn, the flash commands take arguments other than port,
        # current, and to. However, because to is a file, the values of the other
        # arguments does not matter
        if "re-file" in info:
            self.call(
                "flash re",
                f"{self._port} {self._currentMnFw} {info['re-file']} HARDWARE LED",
            )
        if "ex-file" in info:
            self.call(
                "flash ex",
                f"{self._port} {self._currentMnFw} {info['ex-file']} HARDWARE MOTOR",
            )
        if "mn-file" in info:
            self.call(
                "flash mn",
                f"{self._port} {self._currentMnFw} {info['mn-file']} HARDWARE DEV SIDE",
            )

        return 0
