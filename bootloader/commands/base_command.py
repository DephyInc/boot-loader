import sys

from cleo.commands.command import Command

from bootloader.utilities import logo
from bootloader.utilities.system_utils import setup_cache


# ============================================
#                BaseCommand
# ============================================
class BaseCommand(Command):

    _FAILURE: str = ""
    _SUCCESS: str = ""

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self._stylize()
        self._configure_interaction()
        self._configure_unicode()

        setup_cache()

    # -----
    # _styleize
    # -----
    def _stylize(self) -> None:
        self.add_style("info", fg="blue")
        self.add_style("warning", fg="yellow")
        self.add_style("error", fg="red")
        self.add_style("success", fg="green")

    # -----
    # _configure_interaction
    # -----
    def _configure_interaction(self) -> None:
        """
        On some terminals interaction is set to off by default for some
        reason, despite `--no-interaction` not being set. This makes
        sure interactivity is on unless expressly turned off.
        """
        if not self.io.is_interactive() and not self.option("no-interaction"):
            self.io.interactive(True)

    # -----
    # _configure_unicode
    # -----
    def _configure_unicode(self) -> None:
        """
        The marks used to indicate completion status on stdout only
        work if the terminal supports unicode.
        """
        if sys.stdout.encoding.lower().startswith("utf"):  # pylint: disable=no-member
            self._SUCCESS = "<success>✓</success>"
        else:
            self._SUCCESS = "SUCCESS"

    # -----
    # _welcome
    # -----
    def _welcome(self) -> None:
        try:
            self.line(logo.dephyLogo)
        except UnicodeEncodeError:
            self.line(logo.dephyLogoPlain)

        self.line("")
        self.line("Welcome to the Dephy bootloader!")
