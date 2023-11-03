import shutil

import flexsea.utilities.constants as fxc
from cleo.commands.command import Command as BaseCommand
from cleo.helpers import argument

import bootloader.utilities.constants as bc
from bootloader.utilities.help import get_clean_help


# ============================================
#                CleanCommand
# ============================================
class CleanCommand(BaseCommand):
    name = "clean"
    description = "Removes cached files."
    help = get_clean_help()

    arguments = [
        argument(
            "target", "Targets to clean. Can be: `all`, `libs`, `tools`, or `firmware`."
        )
    ]

    # -----
    # handle
    # -----
    def handle(self) -> int:
        target: str = self.argument("target").lower()

        try:
            assert target in ["all", "libs", "tools", "firmware"]
        except AssertionError:
            msg = "<error>Error:</error> the given argument must be one of `all`, "
            msg += "`libs`, `tools`, or `firmware`. See `bootloader clean --help` "
            msg += "for more info."
            self.line("")
            self.line(msg)
            return 1

        if target in ["libs", "all"]:
            self._clean_libs()
        if target in ["tools", "all"]:
            self._clean_tools()
        if target in ["firmware", "all"]:
            self._clean_firmware()

        return 0

    # -----
    # _clean_libs
    # -----
    def _clean_libs(self) -> None:
        shutil.rmtree(fxc.libsPath, ignore_errors=True)

    # -----
    # _clean_tools
    # -----
    def _clean_tools(self) -> None:
        shutil.rmtree(bc.toolsPath, ignore_errors=True)

    # -----
    # _clean_firmware
    # -----
    def _clean_firmware(self) -> None:
        shutil.rmtree(bc.firmwarePath, ignore_errors=True)
