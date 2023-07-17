from botocore.exceptions import ProfileNotFound
from cleo.commands.command import Command as BaseCommand
from cloudpathlib import S3Client

import bootloader.utilities.constants as bc
from bootloader.utilities.help import show_configs_help


# ============================================
#              ShowConfigsCommand
# ============================================
class ShowConfigsCommand(BaseCommand):
    name = "show configs"
    description = "Displays the available pre-made configurations for flashing."
    help = show_configs_help()

    # -----
    # handle
    # -----
    def handle(self) -> int:
        try:
            client = S3Client(profile_name=bc.dephyAwsProfile)
        except ProfileNotFound as err:
            msg = "Error: could not find dephy profile in '~/.aws/credentials'. "
            msg += "Could not list available configs."
            raise RuntimeError(msg) from err

        # We use cloudpathlib here instead of flexsea's get_s3_objects
        # because it's a.) better, b.) separate from flexsea, and c.)
        # because get_s3_objects doesn't work when the objects you're
        # looking for are at the top level of the bucket and not in a
        # sub-folder. In general, I would like to switch to
        # cloudpathlib for all of the S3 operations in both flexsea and
        # the bootloader in the future
        configsPath = client.CloudPath(f"s3://{bc.dephyConfigsBucket}/")

        self.line("Available Configurations")
        self.line("------------------------")

        for config in configsPath.iterdir():
            self.line(f"* {config.name.split('.zip')[0]}")

        self.line("\nPlease use `bootloader flash config <config name>`")

        return 0
