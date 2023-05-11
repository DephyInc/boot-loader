import platform
import sys

from cleo.commands.command import Command

import bootloader.utilities.config as cfg
from bootloader.utilities.system_utils import setup_cache


# ============================================
#                BaseCommand
# ============================================
class BaseCommand(Command):
    """
    Handles configuration of each command.
    """

    _os: str = ""
    _SUCCESS: str = ""

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self._theme: str = ""

        self._configure_unicode()
        setup_cache()

    # -----
    # _setup
    # -----
    def _setup(self) -> None:
        # Not in the constructor because we need access to the run-time options
        self._stylize()
        self._configure_interaction()

        # Not in constructor because we need the `available` command to run anywhere
        self._check_os()

    # -----
    # _stylize
    # -----
    def _stylize(self) -> None:
        try:
            theme = cfg.themes[self._theme]
        except KeyError:
            theme = cfg.themes["classic"]

        for styleName, styleOpts in theme.items():
            self.add_style(styleName, **styleOpts)

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

        if self._os not in cfg.supportedOS:
            raise RuntimeError("Unsupported OS. Run: `bootload show-available --os`")

    # -----
    # handle
    # -----
    def handle(self) -> int:
        raise NotImplementedError
