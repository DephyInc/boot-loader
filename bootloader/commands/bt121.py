import glob
import os
import shutil
import subprocess as sub
from time import sleep

from cleo.helpers import argument
from cleo.helpers import option

import bootloader.utilities.config as cfg
from bootloader.utilities.system_utils import call_flash_tool

from .base_flash_command import BaseFlashCommand


# ============================================
#             FlashBt121Command
# ============================================
class FlashBt121Command(BaseFlashCommand):
    """
    Flashes the bluetooth 121 radio.
    """

    name = "bt121"

    description = "Flashes the bluetooth radio."

    arguments = [
        argument("currentMnFw", "Current firmware version on Manage, e.g., `7.2.0`."),
    ]

    options = [
        option("address", "-a", "BT address. Default is the device id.", flag=False),
        option("baudRate", "-b", "Device baud rate.", flag=False, default=230400),
        option("level", "-L", "GATT level.", flag=False, default=2),
        option("libFile", "-l", "C lib for interacting with Manage.", flag=False),
        option("port", "-p", "Port the device is on, e.g., `COM3`.", flag=False),
    ]

    help = """
    Creates a new bluetooth file with the desired GATT level and flashes it
    onto the device's bt121 radio.

    `--level` is the level of the gatt file to use. Default is 2.

    `--address` is the desired bluetooth address. If not specificed, the device ID
    is used.

    Examples
    --------
    bootload bt121 7.2.0
    bootload bt121 9.1.0 --level 2 --address 0001
    """

    # -----
    # _parse_options
    # -----
    def _parse_options(self) -> None:
        self._currentMnFw = self.argument("currentMnFw")

        self._address = self.option("address")
        self._baudRate = self.option("baudRate")
        self._level = self.option("level")
        self._libFile = self.option("lib")
        self._port = self.option("port")

    # -----
    # _get_target
    # -----
    def _get_target(self) -> None:
        self._target = "bt121"

    # -----
    # _get_firmware_file
    # -----
    def _get_firmware_file(self) -> None:
        """
        Uses the bluetooth tools repo to create a bluetooth image file
        with the correct address.
        """
        self.line("Building bluetooth image...")

        address = self._address if self._address else self._device.deviceId

        # Everything within the bt121 directory is self-contained and
        # self-referencing, so it's easiest to switch to that directory
        # first
        cwd = os.getcwd()
        # The way the zip is decompressed creates this nested structure
        os.chdir(os.path.join(cfg.toolsDir, "bt121_image_tools", "bt121_image_tools"))

        gattTemplate = os.path.join("gatt_files", f"LVL{self._level}.xml")
        gattFile = os.path.join("dephy_gatt_broadcast_bt121", "gatt.xml")

        if not os.path.exists(gattTemplate):
            raise FileNotFoundError(f"Could not find: `{gattTemplate}`.")

        shutil.copyfile(gattTemplate, gattFile)

        if "linux" in self._os:
            pythonCommand = "python3"
        elif "windows" in self._os:
            pythonCommand = "python"
        else:
            raise OSError("Unsupported OS!")

        cmd = [pythonCommand, "bt121_gatt_broadcast_img.py", f"{address}"]
        proc = sub.run(cmd, capture_output=False, check=True, timeout=360)

        if proc.returncode != 0:
            raise RuntimeError("bt121_gatt_broadcast_img.py failed.")

        bgExe = os.path.join("smart-ready-1.7.0-217", "bin", "bgbuild.exe")
        xmlFile = os.path.join("dephy_gatt_broadcast_bt121", "project.xml")
        proc = sub.run([bgExe, xmlFile], capture_output=False, check=True, timeout=360)

        if proc.returncode != 0:
            raise RuntimeError("bgbuild.exe failed.")

        if os.path.exists("output"):
            files = glob.glob(os.path.join("output", "*.bin"))
            for file in files:
                os.remove(file)
        else:
            os.mkdir("output")

        btImageFile = f"dephy_gatt_broadcast_bt121_Exo-{self._address}.bin"
        shutil.move(os.path.join("dephy_gatt_broadcast_bt121", btImageFile), "output")
        btImageFile = os.path.join(os.getcwd(), "output", btImageFile)

        os.chdir(cwd)

        self._fwFile = btImageFile
        self.line(f"Building bluetooth image... {self._SUCCESS}")

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        self._flashCmd = [
            os.path.join(cfg.toolsDir, "stm32flash"),
            "-w",
            f"{self._fwFile}",
            "-b",
            "115200",
            self._device.port,
        ]

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        self._device.close()
        sleep(3)
        call_flash_tool(self._flashCmd)
        sleep(20)
