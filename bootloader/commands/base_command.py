import sys

from cleo.commands.command import Command
from flexsea.utilities.system import get_os

import bootloader.utilities.constants as blc


# ============================================
#                BaseCommand
# ============================================
class BaseCommand(Command):
    """
    Contains command configuration.
    """

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self._os: str = ""
        self._SUCCESS: str = ""
        self._theme: str = ""

        self._check_os()
        self._configure_unicode()

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
        self._os = get_os()

        if self._os not in cfg.supportedOS:
            raise RuntimeError("Unsupported OS. Run: `bootload show-available --os`")

    # -----
    # _configure_interaction
    # -----
    def _configure_interaction(self) -> None:
        """
        On some terminals interaction is set to off by default for some
        reason, despite `--no-interaction` not being set. This makes
        sure interactivity is on unless expressly turned off.
        """
        # Not called in the constructor because it requires the
        # --no-interaction cli option and io attribute, which aren't 
        # available at construction time
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
    # _stylize
    # -----
    def _stylize(self) -> None:
        # Not called in the constructor because it requires the --theme 
        # cli option, which isn't available at construction time
        try:
            theme = cfg.themes[self._theme]
        except KeyError:
            theme = cfg.themes["classic"]

        for styleName, styleOpts in theme.items():
            self.add_style(styleName, **styleOpts)

    # -----
    # handle
    # -----
    def handle(self) -> int:
        raise NotImplementedError
