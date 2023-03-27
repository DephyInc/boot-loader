from typing import List

from cleo.helpers import option

import bootloader.utilities.config as cfg

from bootloader.utilities.aws import get_s3_object_info

from .base_command import BaseCommand


# ============================================
#                 ShowCommand
# ============================================
class ShowCommand(BaseCommand):
    """
    Shows firmware, devices, and hardware available for bootloading.
    """

    name = "show-available"

    description = "Shows firmware, devices, and hardware available for bootloading."

    options = [
        option("devices", "-d", "Show devices that can be bootloaded.", flag=True),
        option("hardware", "-r", "Show available hardware versions.", flag=True),
        option("firmware", None, "Show firmware versions.", flag=True),
        option("c-libraries", None, "Show available C libraries.", flag=True),
    ]

    help = """
    Displays the devices, hardware versions, firmware versions, and versions
    of the pre-compiled C libraries that are available for bootloading.

    Examples
    --------
    # Show all
    > bootload show-available

    # Show only devices
    > bootload show-available --devices
    """

    # -----
    # handle
    # -----
    def handle(self) -> int:
        """
        Entry point for the command.
        """
        self._stylize()
        self._configure_interaction()

        showDevices = self.option("devices")
        showHardware = self.option("hardware")
        showFirmware = self.option("firmware")
        showLibraries = self.option("c-libraries")

        _all = not (showDevices or showHardware or showFirmware or showLibraries)

        fwInfo = get_s3_object_info(cfg.firmwareBucket, cfg.dephyProfile)
        libsInfo = get_s3_object_info(cfg.libsBucket)

        if showDevices:
            self._list_devices(fwInfo)
        if showHardware:
            self._list_hardware(fwInfo)
        if showFirmware:
            self._list_firmware(fwInfo)
        if showLibraries:
            self._list_libraries(libsInfo)
        if _all:
            self._list_all(fwInfo)
            self._list_libraries(libsInfo)

        return 0

    # -----
    # _list_devices
    # -----
    def _list_devices(self, info: dict) -> None:
        devices = set()

        for versionDict in info.values():
            for deviceSet in versionDict.values():
                devices.update(deviceSet)

        self.line("Available devices:")
        for device in devices:
            self.line(f"\t- <info>{device}</info>")

    # -----
    # _list_hardware
    # -----
    def _list_hardware(self, info: dict) -> None:
        hardware = set()

        for versionDict in info.values():
            for hw in versionDict:
                hardware.add(hw)

        self.line("Available hardware:")
        for hw in hardware:
            self.line(f"\t- <info>{hw}</info>")

    # -----
    # _list_firmware
    # -----
    def _list_firmware(self, info: dict) -> None:
        self.line("Available versions:")
        for version in info:
            self.line(f"\t- <info>{version}</info>")

    # -----
    # _list_libraries
    # -----
    def _list_libraries(self, libs: List[str]) -> None:
        self.line("Available pre-compiled C libraries:")
        for lib in libs:
            self.line(f"\t- <info>{lib}</info>")

    # -----
    # _list_all
    # -----
    def _list_all(self, info: dict) -> None:
        pad = "    "

        for version in info:
            self.line(f"<info>Version</info>: {version}")
            for hw, devices in info[version].items():
                self.line(f"{pad}<info>Hardware</info> {hw}")
                for device in devices:
                    self.line(f"{pad}{pad}- <warning>{device}</warning>")
