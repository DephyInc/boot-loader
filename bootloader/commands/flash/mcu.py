from pathlib import Path
import sys

from cleo.helpers import argument
from flexsea.utilities.firmware import validate_given_firmware_version

from bootloader.commands.flash.base_flash import BaseFlashCommand


# ============================================
#              FlashMcuCommand
# ============================================
class FlashMcuCommand(BaseFlashCommand):
    """
    Flashing Mn, Ex, and Re is extremely similar, so this class
    contains the shared functionality.
    """

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self.arguments.append(
            argument("to", "Version to flash, e.g., `9.1.0`, or path to file to use.")
        )
        self.arguments.append(
            argument("rigidVersion", "PCB hardware version, e.g., `4.1B`.")
        )

        self._to: str = ""
        self._rigidVersion: str = ""

    # -----
    # _parse_options
    # -----
    def _parse_options(self) -> None:
        super()._parse_options()

        self._to = self.argument("to")
        self._rigidVersion = self.argument("rigidVersion")

    # -----
    # _get_firmware_file
    # -----
    def _get_firmware_file(self) -> None:
        # If self._to is a file instead of a version string,
        # validate_given_firmware_version raises a ValueError
        try:
            desiredFirmwareVersion = validate_given_firmware_version(
                self._to, not self.option("no-interaction")
            )
        except ValueError:
            self._handle_firmware_file()
        else:
            self._handle_firmware_version(desiredFirmwareVersion)

    # -----
    # _handle_firmware_file
    # -----
    def _handle_firmware_file(self) -> None:
        self._fwFile = Path(self._to).expanduser().resolve()
        if not self._fwFile.is_file():
            raise RuntimeError(f"Error: could not find given firmware file: {self._to}")

    # -----
    # _confirm
    # -----
    def _confirm(self) -> None:
        self.line(f"\t* Flashing target: {self._target}")
        self.line(f"\t* To: {self._to}")
        msg = "\t* Using Mn firmware version for communication with target: "
        msg += f"{self._currentMnFw}"
        self.line(msg)
        self.line(f"\t* Device's rigid version: {self._rigidVersion}")

        if not self.option("no-interaction"):
            if not self.confirm("Proceed?"):
                self.line("<error>Aborting.</>")
                sys.exit(1)

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        raise NotImplementedError

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        raise NotImplementedError

    # -----
    # _handle_firmware_version
    # -----
    def _handle_firmware_version(self, version: Version) -> None:
        raise NotImplementedError
