from pathlib import Path
import sys
from typing import List

from cleo.commands.command import Command as BaseCommand
from cleo.helpers import argument
from cleo.helpers import option
from flexsea.device import Device


# ============================================
#              BaseFlashCommand
# ============================================
class BaseFlashCommand(BaseCommand):
    """
    Flashing each target is extremely similar, so this class
    contains the shared functionality.
    """

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self.arguments = [
            argument("port", "Port the device is on, e.g., `COM3`."),
            argument("currentMnFw", "Manage's current firmware, e.g., `7.2.0`."),
        ]

        self.options = [
            option("baudRate", "-b", "Device baud rate.", flag=False, default=230400),
            option("libFile", "-l", "C lib for interacting with Manage.", flag=False),
        ]

        self._port: str = ""
        self._currentMnFw: str = ""
        self._baudRate: int = 0
        self._libFile: str = ""
        self._target: str = ""
        self._device: Device | None = None
        self._fwFile: Path | str | None = None
        self._flashCmd: List[str] | None = None

        self.hidden = True

    # -----
    # handle
    # -----
    def handle(self) -> int:
        """
        Entry point for the command.
        """
        self._parse_options()
        self.call("download tools", f"{self._target} {self.application._os}")
        self._get_device()
        self._get_firmware_file()
        self._get_flash_command()
        self._confirm()
        self._set_tunnel_mode()
        self._flash()

        return 0

    # -----
    # _parse_options
    # -----
    def _parse_options(self) -> None:
        self._port = self.argument("port")
        self._currentMnFw = self.argument("currentMnFw")
        self._baudRate = int(self.option("baudRate"))
        self._libFile = self.option("libFile")

    # -----
    # _get_device
    # -----
    def _get_device(self) -> None:
        """
        Creates an instance of the `Device` class and opens it.
        """
        self.write("</info>Connecting</> to device...")

        self._device = Device(
            self._currentMnFw,
            self._port,
            baudRate=self._baudRate,
            libFile=self._libFile,
            interactive=not self.option("no-interaction"),
        )

        self._device.open()

        self.overwrite(f"</info>Connecting</> to device... {self.application._SUCCESS}")

    # -----
    # _set_tunnel_mode
    # -----
    def _set_tunnel_mode(self) -> None:
        """
        Puts Manage into tunnel mode so that we can communicate to the
        desired target through Manage.
        """
        if not self.option("no-interaction"):
            msg = "<warning>Please make sure the battery is removed "
            msg += "and/or the power supply is disconnected!</warning>"

            if not self.confirm(msg, False):
                sys.exit(1)

        self.write(f"<info>Setting</> tunnel mode for {self._target}...")

        if not self._device.set_tunnel_mode(self._target, 20):
            msg = "\n<error>Error</error>: failed to activate bootloader for: "
            msg += f"<info>`{self._target}`</info>"
            self.line(msg)
            sys.exit(1)

        msg = f"<info>Setting</> tunnel mode for {self._target}... "
        msg += f"{self.application._SUCCESS}\n"
        self.overwrite(msg)

    # -----
    # _flash
    # -----
    def _flash(self) -> None:
        """
        Calls the appropriate executable for flashing the desired target.
        """
        self.write(f"<info>Flashing</> {self._target}...")

        self._flash_target()

        if not (self.option("no-interaction") or self.option("quiet")):
            if not self.confirm("Please power cycle device.", False):
                sys.exit(1)

        self.overwrite(
            f"<info>Flashing</> {self._target}... {self.application._SUCCESS}\n"
        )

    # -----
    # _get_firmware_file
    # -----
    def _get_firmware_file(self) -> None:
        raise NotImplementedError

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        raise NotImplementedError

    # -----
    # _confirm
    # -----
    def _confirm(self) -> None:
        raise NotImplementedError

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        raise NotImplementedError
