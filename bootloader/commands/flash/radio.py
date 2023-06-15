from time import sleep

from cleo.helpers import option

from bootloader.utilities.system_utils import call_flash_tool

from .base_flash import BaseFlashCommand


# ============================================
#              FlashRadioCommand
# ============================================
class FlashRadioCommand(BaseFlashCommand):
    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self.options.append(
            option(
                "address", None, "Bluetooth address. Default is device id.", flag=False
            )
        )

        self._address: str = ""

        self.hidden = True

    # -----
    # _parse_options
    # -----
    def _parse_options(self) -> None:
        super()._parse_options()

        self._address = self.option("address")

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
        self.line(f"\t* Flashing target: {self._target}")
        self.line(f"\t* Setting bluetooth address as: {self._address}")
        msg = "\t* Using Mn firmware version for communication with target: "
        msg += f"{self._currentMnFw}"
        self.line(msg)

        super()._confirm()

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
