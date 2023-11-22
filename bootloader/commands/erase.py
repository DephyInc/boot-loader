from cleo.commands.command import Command as BaseCommand

import bootloader.utilities.constants as bc
from bootloader.utilities.help import erase_help
from bootloader.utilities.system_utils import run_command


# ============================================
#                EraseCommand
# ============================================
class EraseCommand(BaseCommand):
    name = "erase"
    description = "Performs a full chip erase on Mn."
    help = erase_help()

    # -----
    # handle
    # -----
    def handle(self) -> int:
        self.line(erase_help())
        self.line("")

        if not self.option("no-interaction"):
            self.line("")
            self.line("")

            if not self.confirm("Proceed?"):
                msg = "Aborting chip erase. If this abort happened without your input, "
                msg += "and you are sure you want to proceed with this operation, try "
                msg += "re-running with the `--no-interaction` option."
                self.line(msg)

                return 1

        dirName = (
            "stlink-1.7.0-i686-w64-mingw32"
            if "32bit" in self.application._os
            else "stlink-1.7.0-x86_64-w64-mingw32"
        )

        executable = str(
            bc.toolsPath.joinpath(
                self.application._os,
                "stlink-1",
                dirName,
                "bin",
                "st-flash.exe",
            )
        )

        run_command([f"{executable}", "erase"])

        return 0
