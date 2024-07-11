from cleo.commands.command import Command as BaseCommand
from cleo.helpers import argument
from cloudpathlib import S3Client

import bootloader.utilities.constants as bc
from bootloader.utilities.help import config_rename_help


# ============================================
#            ConfigRenameCommand
# ============================================
class ConfigRenameCommand(BaseCommand):
    name = "config rename"
    description = "Changes the name of an existing config."
    help = config_rename_help()

    arguments = [
        argument("originalName", "Current name of the configuration."),
        argument("newName", "New name of the configuration."),
    ]

    # -----
    # handle
    # -----
    def handle(self) -> int:
        originalName = self.argument("originalName")
        newName = self.argument("newName")

        client = S3Client(profile_name=bc.dephyAwsProfile)

        originalPath = client.CloudPath(
            f"s3://{bc.dephyConfigsBucket}/{originalName}.zip"
        )
        newPath = client.CloudPath(f"s3://{bc.dephyConfigsBucket}/{newName}.zip")

        if not originalPath.exists():
            self.line(f"Could not rename: {originalName} does not exist.")
            return 1

        originalPath.rename(newPath)

        self.line(f"Renaming: {self.application._SUCCESS}")

        return 0
