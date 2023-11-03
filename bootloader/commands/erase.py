from cleo.commands.command import Command as BaseCommand

from bootloader.utilities.help import erase_help


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
        return 0
