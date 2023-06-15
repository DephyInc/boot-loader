from cleo.helpers import argument
from cleo.helpers import option

from .base_flash import BaseFlashCommand


# ============================================
#              FlashXbeeCommand
# ============================================
class FlashXbeeCommand(BaseFlashCommand):
    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self.name = "flash xbee"
        self.description = "Flashes new firmware onto xbee."
        self.help = self._help()

        self.arguments.append(
            argument("buddyAddress", "Bluetooth address of device's pair.")
        )

        self.options.append(
            option(
                "address", None, "Bluetooth address. Default is device id.", flag=False
            )
        )

        self._address: str = ""
        self._buddyAddress: str = ""

        self.hidden = False

    # -----
    # _parse_options
    # -----
    def _parse_options(self) -> None:
        super()._parse_options()

        self._address = self.option("address")
        self._buddyAddress = self.argument("buddyAddress")
        self._target = "xbee"

    # -----
    # _get_firmware_file
    # -----
    def _get_firmware_file(self) -> None:
        """
        Uses the bluetooth tools repo to create a bluetooth image file
        with the correct address.
        """
        # A firmware file isn't required for xbee
        pass

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        if "windows" in self._os:
            pythonCmd = "python"
        else:
            pythonCmd = "python3"

        address = self._address if self._address else self._device.deviceId

        self._flashCmd = [
            pythonCmd,
            os.path.join(cfg.toolsPath, "xb24c.py"),
            self._port,
            address,
            self._buddyAddress,
            "upgrade",
        ]

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        self._device.close()
        sleep(3)
        call_flash_tool(self._flashCmd)
        sleep(20)

    # -----
    # _confirm
    # -----
    def _confirm(self) -> None:
        self.line("<info>Summary</>:")
        self.line(f"\t* Flashing target: {self._target}")
        self.line(f"\t* Setting bluetooth address as: {self._address}")
        self.line(f"\t* Setting buddy bluetooth address as: {self._buddyAddress}")
        self.line(
            f"\t* Using Mn firmware version for communication with target: {self._currentMnFw}"
        )

        if not self.option("no-interaction"):
            if not self.confirm("Proceed?"):
                self.line("<error>Aborting.</>")
                sys.exit(1)

    # -----
    # _help
    # -----
    def _help(self) -> str:
        return "Flashes new firmware onto xbee."
