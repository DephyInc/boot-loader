import platform
import sys

from cleo.commands.command import Command

from bootloader.exceptions.exceptions import UnsupportedOSError
import bootloader.utilities.config as cfg
from bootloader.utilities.system_utils import setup_cache


# ============================================
#                BaseCommand
# ============================================
class BaseCommand(Command):
    _os: str = ""
    _SUCCESS: str = ""

    # -----
    # _setup
    # -----
    def _setup(self) -> None:
        self._stylize()
        self._configure_interaction()
        self._configure_unicode()
        self._check_os()
        setup_cache()

    # -----
    # _stylize
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
        The checkmarks used to indicate successful completion on stdout
        only work if the terminal supports unicode.
        """
        if sys.stdout.encoding.lower().startswith("utf"):  # pylint: disable=no-member
            self._SUCCESS = "<success>✓</success>"
        else:
            self._SUCCESS = "SUCCESS"

    # -----
    # _check_os
    # -----
    def _check_os(self) -> None:
        """
        Makes sure we're running on a supported OS.

        Raises
        ------
        UnsupportedOSError
            If the detected operating system is not supported.
        """
        self._os = platform.system().lower()

        try:
            assert self._os in cfg.supportedOS
        except AssertionError as err:
            raise UnsupportedOSError(self._os, cfg.supportedOS) from err

    # -----
    # handle
    # -----
    def handle(self) -> int:
        raise NotImplementedError
