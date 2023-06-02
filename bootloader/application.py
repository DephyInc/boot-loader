from typing import List

from cleo.application import Application
from cleo.commands.command import Command

from bootloader import __version__
from bootloader.commands.all import FlashAllCommand
from bootloader.commands.bt121 import FlashBt121Command
from bootloader.commands.config import CreateConfigurationCommand
from bootloader.commands.ex import FlashExecuteCommand
from bootloader.commands.habs import FlashHabsCommand
from bootloader.commands.mn import FlashManageCommand
from bootloader.commands.re import FlashRegulateCommand
from bootloader.commands.show import ShowAvailableCommand
from bootloader.commands.xbee import FlashXbeeCommand


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
            CreateConfigurationCommand,
            FlashAllCommand,
            FlashBt121Command,
            FlashExecuteCommand,
            FlashHabsCommand,
            FlashManageCommand,
            FlashRegulateCommand,
            FlashXbeeCommand,
            ShowAvailableCommand,
        ]

        return commandList
