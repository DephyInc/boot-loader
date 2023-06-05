from importlib import import_module

from cleo.application import Application as BaseApplication
from cleo.formatters.style import Style
from cleo.helpers import option
from cleo.io.io import IO

from bootloader import __version__
from bootloader.command_list import COMMANDS
import bootloader.utilities.constants as bc


# ============================================
#                 Application
# ============================================
class Application(BaseApplication):

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__("bootload", __version__)

        self._load_commands()

    # -----
    # _load_commands
    # -----
    def _load_commands(self) -> None:
        """
        This saves us from having to import lots of classes. The names
        of the commands match the names of the files, and by nesting
        directories in the `commands` directory we can have multi-word
        commands. E.g., `commands/env/create.py` would be the command
        `bootload env create`. The name in `COMMANDS` would be 
        'env create'.
        """
        for name in COMMANDS:
            words = name.split(" ")
            module = import_module("bootloader.commands." + ".".join(words))
            cmdClass = getattr(module, "".join(c.title() for c in words) + "Command")
            command = cmdClass()
            self.add(command)

    # -----
    # _default_definition
    # -----
    @property
    def _default_definition(self):
        """
        This is an override of cleo's method. It's where 
        application-level options such as `--quiet` and `--verbose`
        are set. Here we override it in order to add the `--theme`
        option so each command does not need to be configured 
        individually.
        """
        definition = super()._default_definition
        opt = option("--theme", "-t", "Sets theme.", flag=False)
        definition.add_option(opt)
        return definition

    # -----
    # _configure_io
    # -----
    def _configure_io(self, io: IO) -> None:
        """
        Whenever a command's `run` method is called, cleo calls 
        `_create_io` and `_configure_io`. Here we override 
        `configure_io` to be able to configure the theme of each 
        command.
        """
        # This actually parses the command-line to give each option a 
        # value
        io.input.bind(self.definition)

        theme = io.input.option("theme")
        try:
            assert theme in bc.themes
        except AssertionError:
            theme = "default"

        formatter = io.output.formatter

        for styleName, styleOpts in bc.themes[theme].items():
            formatter.set_style(styleName, Style(**styleOpts))

        io.output.set_formatter(formatter)
        io.error_output.set_formatter(formatter)

        super()._configure_io(io)
