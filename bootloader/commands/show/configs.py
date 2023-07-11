import boto3
from botocore.exceptions import ProfileNotFound
from cleo.commands.command import Command as BaseCommand
from flexsea.utilities.aws import get_s3_objects

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
            client = boto3.Session(profile_name=bc.dephyAwsProfile).client("s3")
        except ProfileNotFound as err:
            msg = "Error: could not find dephy profile in '~/.aws/credentials'. "
            msg += "Could not list available configs."
            raise RuntimeError(msg) from err

        configs = get_s3_objects(bc.dephyConfigsBucket, client)

        self.line("Available Configurations")
        self.line("------------------------")

        for config in configs:
            self.line(f"* {config}")

        self.line("\nPlease use `bootloader flash config <config name>`")

        return 0
