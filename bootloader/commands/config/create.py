from cleo.commands.command import Command as BaseCommand
from cleo.helpers import argument
from cleo.helpers import option
import pendulum

from bootloader.utilities.help import config_create_help


# ============================================
#           ConfigCreateCommand
# ============================================
class ConfigCreateCommand(BaseCommand):
    name = "config create"
    description = "Creates a collection of files that can be flashed via `flash config`"
    help = config_create_help()

    arguments = [argument("configName", "Name of the configuration.")]

    options = [
        option("mn-file", None, "File to use for Manage.", flag=False),
        option("ex-file", None, "File to use for Execute.", flag=False),
        option("re-file", None, "File to use for Regulate.", flag=False),
        option("firmware-version", None, "Version of C library to use.", flag=False),
        option("lib-file", None, "C library file to use.", flag=False),
    ]

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self._mnFile: str = ""
        self._exFile: str = ""
        self._reFile: str = ""
        self._firmwareVersion: str = ""
        self._libFile: str = ""
        self._configName: str = ""

    # -----
    # handle
    # -----
    def handle(self) -> int:
        self._configName = self.argument("configName") + f"{pendulum.today()}"
        self._mnFile = 
        return 0
