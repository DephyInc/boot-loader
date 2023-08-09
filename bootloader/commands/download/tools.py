import os
from pathlib import Path
import subprocess as sub
import sys
import zipfile

from cleo.commands.command import Command as BaseCommand
from cleo.helpers import argument
from flexsea.utilities.aws import s3_download
import flexsea.utilities.constants as fxc

import bootloader.utilities.constants as bc
from bootloader.utilities.help import tools_help
from bootloader.utilities.system_utils import run_command


# ============================================
#           DownloadToolsCommand
# ============================================
class DownloadToolsCommand(BaseCommand):
    name = "download tools"
    description = "Downloads the 3rd party tools needed to bootload the target."
    help = tools_help()
    hidden = False

    arguments = [
        argument("target", "The target to get tools for, e.g., mn, ex, or re."),
    ]

    # -----
    # handle
    # -----
    def handle(self) -> int:
        opSys = self.application._os

        for tool in bc.bootloaderTools[opSys][self.argument("target")]:
            self.write(f"Searching for: <info>{tool}</info>...")

            dest = bc.toolsPath.joinpath(opSys, tool)

            if not dest.exists():
                self.line(f"\n\t<info>{tool}</info> <warning>not found.</warning>")
                self.write("\tDownloading...")
                dest.parent.mkdir(parents=True, exist_ok=True)

                toolObj = str(Path(bc.toolsDir).joinpath(opSys, tool).as_posix())
                s3_download(toolObj, fxc.dephyPublicFilesBucket, str(dest))

                if zipfile.is_zipfile(dest):
                    with zipfile.ZipFile(dest, "r") as archive:
                        base = dest.name.split(".")[0]
                        extractedDest = Path(os.path.dirname(dest)).joinpath(base)
                        archive.extractall(extractedDest)

                self.overwrite(f"\tDownloading... {self.application._SUCCESS}\n")

            else:
                msg = f"Searching for: <info>{tool}</info>..."
                msg += f"{self.application._SUCCESS}\n"
                self.overwrite(msg)

        if self.argument("target") == "setup":
            dfusePath = str(
                bc.toolsPath.joinpath(opSys, "dfuse_command", "dfuse_v3.0.6", "Bin")
            )
            mingwPath = str(
                bc.toolsPath.joinpath(
                    opSys,
                    "mingw",
                    "mingw-w64",
                    "mingw-w64",
                    "i68608.1.0-posix-dwarf-rt_v6-rev0",
                    "mingw32",
                    "bin",
                )
            )
            os.environ["PATH"] += dfusePath
            os.environ["PATH"] += mingwPath
            if not bc.firstSetup.is_file():
                msg = "We're about to install ST Link. At the end of the installation "
                msg += "process, a window will pop up asking you to install the STM "
                msg += "drivers. <warning>You MUST install these or bootloading will "
                msg += "not work.</warning>"
                self.line(msg)
                if not self.confirm("Proceed?"):
                    self.line(
                        "Acknowledgment of need to install drivers not given. Aborting."
                    )
                    sys.exit(1)
                cmd = [
                    str(bc.toolsPath.joinpath(opSys, "stlink_setup.exe")),
                ]
                try:
                    run_command(cmd)
                except (RuntimeError, sub.TimeoutExpired):
                    self.line("Error: could not install STM drivers.")
                    sys.exit(1)
        self.line("")

        return 0
