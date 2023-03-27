import sys
from typing import List

from flexsea.device import Device

from bootloader.utilities.system_utils import get_flash_tools

from .base_command import BaseCommand


# ============================================
#             BaseFlashCommand
# ============================================
class BaseFlashCommand(BaseCommand):
    """
    Contains all the functionality shared by every flash command.
    """

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self._address: str = ""
        self._baudRate: int = -1
        self._buddyAddress: str = ""
        self._currentMnFw: str = ""
        self._device: Device | None = None
        self._deviceName: str = ""
        self._flashCmd: List[str] = []
        self._fwFile: str = ""
        self._libFile:str = ""
        self._port:str = ""
        self._rigidVersion: str = ""
        self._side: str = ""
        self._target: str = ""
        self._to: str = ""

    # -----
    # handle
    # -----
    def handle(self) -> int:
        """
        Entry point for the command.
        """
        self._setup()
        self._parse_options()
        self._get_target()
        get_flash_tools(self._target, self._os)
        self._get_device()
        self._get_firmware_file()
        self._get_flash_command()
        self._set_tunnel_mode()
        self._flash()

        return 0

    # -----
    # _get_device
    # -----
    def _get_device(self) -> None:
        """
        Creates an instance of the `Device` class and opens it.
        """
        self._device = Device(
            port=self._port,
            baudRate=self._baudRate,
            cLibVersion=self._from,
            libFile=self._libFile,
        )

        self._device.open()
        # self._port holds the value of the --port option. If none is given, we use
        # the one auto-detected by Device.open()
        self._port = self._port if self._port else self._device.port

    # -----
    # _set_tunnel_mode
    # -----
    def _set_tunnel_mode(self) -> None:
        """
        Puts Manage into tunnel mode so that we can communicate to the
        desired target through Manage.
        """
        if not (self.option("no-interaction") or self.option("quiet")):
            msg = "<warning>Please make sure the battery is removed "
            msg += "and/or the power supply is disconnected!</warning>"

            if not self.confirm(msg, False):
                sys.exit(1)

        self.write(f"Setting tunnel mode for {self._target}...")

        if not self._device.set_tunnel_mode(self._target, 20):
            msg = "\n<error>Error</error>: failed to activate bootloader for: "
            msg += f"<info>`{self._target}`</info>"
            self.line(msg)
            sys.exit(1)

        self.overwrite(f"Setting tunnel mode for {self._target}... {self._SUCCESS}\n")

    # -----
    # _flash
    # -----
    def _flash(self) -> None:
        """
        Calls the appropriate executable for flashing the desired target.
        """
        self.write(f"Flashing {self._target}...")

        self._flash_target()

        if not (self.option("no-interaction") or self.option("quiet")):
            if not self.confirm("Please power cycle device.", False):
                sys.exit(1)

        self.overwrite(f"Flashing {self._target}... {self._SUCCESS}\n")

    # -----
    # _parse_options
    # -----
    def _parse_options(self) -> None:
        """
        Sets values of options and arguments to instance attributes.

        Should be implemented by the Child class.
        """
        raise NotImplementedError

    # -----
    # _get_target
    # -----
    def _get_target(self) -> None:
        """
        Gets the desired target to flash.

        Should be implemented by the Child class.
        """
        raise NotImplementedError

    # -----
    # _get_flash_tools
    # -----
    def _get_flash_tools(self) -> None:
        """
        Checks if the required tools are installed. If not, we download
        them from S3.

        Should be implemented by the Child class.
        """
        raise NotImplementedError

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        """
        Constructs a list of strings containing the invocation of requisite
        tool needed to flash the desired target.

        Should be implemented by the Child class.
        """
        raise NotImplementedError

    # -----
    # _get_firmware_file
    # -----
    def _get_firmware_file(self) -> None:
        """
        Either uses the given file or constructs and, if necessary, downloads
        the requisite file from S3.

        Should be implemented by the Child class.
        """
        raise NotImplementedError

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        """
        Invokes the target-specific flash tool.

        Should be implemented by the Child class.
        """
        raise NotImplementedError
