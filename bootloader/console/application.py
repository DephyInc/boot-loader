from typing import List

from cleo.application import Application
from cleo.commands.command import Command

from bootloader import __version__


# ============================================
#          BootloaderApplication
# ============================================
class BootloaderApplication(Application):
    """
    The CLI object. Adds and runs each available command.
    """

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__("bootload", __version__)

        for cmd in self._get_commands():
            self.add(cmd())

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
        ]

        return commandList
