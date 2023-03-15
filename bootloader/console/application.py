from typing import List

from cleo.application import Application
from cleo.commands.command import Command

from bootloader import __version__

from bootloader.commands.all import FlashAllCommand
from bootloader.commands.flash_bt121 import FlashBt121Command
from bootloader.commands.flash_ex import FlashExecuteCommand
from bootloader.commands.flash_habs import FlashHabsoluteCommand
from bootloader.commands.flash_mn import FlashManageCommand
from bootloader.commands.flash_re import FlashRegulateCommand
from bootloader.commands.flash_xbee import FlashXbeeCommand
from bootloader.commands.show import ShowCommand


# ============================================
#           BootloaderApplication
# ============================================
class BootloaderApplication(Application):
    """
    The CLI object.
    """

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__("bootload", __version__)

        for command in self._get_commands():
            self.add(command())

    # -----
    # _get_commands
    # -----
    def _get_commands(self) -> List[Command]:
        """
        Helper method for telling the CLI about the commands available to
        it.

        Returns
        -------
        commandList : List[Command]
            A list of commands available to the CLI.
        """
        commandList = [
            FlashAllCommand,
            FlashBt121Command,
            FlashExecuteCommand,
            FlashHabsoluteCommand,
            FlashManageCommand,
            FlashRegulateCommand,
            FlashXbeeCommand,
            ShowCommand,
        ]

        return commandList
