import glob
import os
import shutil
import subprocess as sub
from time import sleep
from typing import List

from cleo.helpers import option

import bootloader.utilities.config as cfg

from .flash_mcu import FlashMcuCommand


# ============================================
#             FlashBt121Command
# ============================================
class FlashBt121Command(FlashMcuCommand):
    """
    Flashes the bluetooth 121 radio.
    """

    name = "bt121"

    description = "Flashes the bluetooth radio."

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

    _address: str = ""
    _level: int = -1
    _target: str = "bt"

    # -----
    # __new__
    # -----
    def __new__(cls):
        obj = super().__new__(cls)
        _ = obj.arguments.pop()
        obj.options.append(option("address", "-a", "Bt121 address.", flag=False))
        obj.options.append(option("level", None, "GATT level.", flag=False, default=2))

        return obj

    # -----
    # _get_firmware_file
    # -----
    def _get_firmware_file(self) -> None:
        """
        Uses the bluetooth tools repo (downloaded as a part of `init`)
        to create a bluetooth image file with the correct address.
        """
        self._level = self.option("level")
        if self.option("address"):
            self._address = self.option("address")
        else:
            self._address = self._device.deviceId

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

        if self._os == "windows":
            pythonCommand = "python"
        else:
            pythonCommand = "python3"

        cmd = [pythonCommand, "bt121_gatt_broadcast_img.py", f"{self._address}"]
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

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        self._device.close()
        sleep(3)
        self._call_flash_tool()
        sleep(20)

    # -----
    # _flashCmd
    # -----
    @property
    def _flashCmd(self) -> List[str]:
        cmd = [
            os.path.join(cfg.toolsDir, "stm32flash"),
            "-w",
            f"{self._fwFile}",
            "-b",
            "115200",
            self._device.port,
        ]

        return cmd
