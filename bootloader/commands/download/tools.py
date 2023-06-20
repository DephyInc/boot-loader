import os
from pathlib import Path
import zipfile

from cleo.commands.command import Command as BaseCommand
from cleo.helpers import argument
from flexsea.utilities.aws import s3_download
import flexsea.utilities.constants as fxc

import bootloader.utilities.constants as bc


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

        for tool in bc.bootloaderTools[opSys]:
            self.write(f"Searching for: <info>{tool}</info>...")

            dest = bc.toolsPath.joinpath(opSys, tool)

            if not dest.exists():
                self.line(f"\n\t<info>{tool}</info> <warning>not found.</warning>")
                self.write("\tDownloading...")

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

        return 0


# ============================================
#                  tools_help
# ============================================
def tools_help() -> str:
    return "Downloads tools for bootloading."
