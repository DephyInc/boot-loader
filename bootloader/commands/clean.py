from cleo.commands.command import Command as BaseCommand
from cleo.helpers import argument

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
