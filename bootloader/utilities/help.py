# ============================================
#                  mn_help
# ============================================
def mn_help() -> str:
    return "Flashes new firmware onto Manage."


# ============================================
#                  ex_help
# ============================================
def ex_help() -> str:
    return "Flashes new firmware onto Execute."


# ============================================
#                  re_help
# ============================================
def re_help() -> str:
    return "Flashes new firmware onto Regulate."


# ============================================
#                  habs_help
# ============================================
def habs_help() -> str:
    return "Flashes new firmware onto Habsolute."


# ============================================
#                  bt121_help
# ============================================
def bt121_help() -> str:
    return "Flashes new firmware onto Bt121."


# ============================================
#                  xbee_help
# ============================================
def xbee_help() -> str:
    return "Flashes new firmware onto Bt121."


# ============================================
#                  all_help
# ============================================
def all_help() -> str:
    return "Flashes new firmware onto xbee, bt121, habs, ex, re, and mn."


# ============================================
#                  tools_help
# ============================================
def tools_help() -> str:
    return "Downloads tools for bootloading."


# ============================================
#             config_create_help
# ============================================
def config_create_help() -> str:
    return "Creates a collection of files that can be flashed via `flash config`"


# ============================================
#             show_configs_help
# ============================================
def show_configs_help() -> str:
    return "Displays the available pre-made configurations for flashing."


# ============================================
#             flash_config_help
# ============================================
def flash_config_help() -> str:
    return "Flashes the files stored in the given config."


# ============================================
#            config_download_help
# ============================================
def config_download_help() -> str:
    return "Downloads the given configuration from S3."


# ============================================
#            config_upload_help
# ============================================
def config_upload_help() -> str:
    return "Uploads the given configuration to S3."


# ============================================
#            show_devices_help
# ============================================
def show_devices_help() -> str:
    return "Lists all devices for which there is firmware."


# ============================================
#            show_rigids_help
# ============================================
def show_rigids_help() -> str:
    return "Lists all rigid versions for which there is firmware."


# ============================================
#            show_versions_help
# ============================================
def show_versions_help() -> str:
    return "Lists all available firmware versions."


# ============================================
#                 clean_help
# ============================================
def clean_help() -> str:
    msg = "Removes the `target` directory. `target` can be: `all`, `libs`, `tools`\n"
    msg += "or `firmware`.\n\nIf `target` is `libs`, all of the cached pre-compiled\n"
    msg += "C libraries will be removed.\n\nIf `target` is `tools`, then all of the\n"
    msg += "cached tools necessary for bootloading will be removed. This will force\n"
    msg += "them to be re-downloaded.\n\nIf `target` is firmware, the all of the\n"
    msg += "cached firmware files will be removed.\n\nIf `target` is `all`, then all\n"
    msg += "of the above operations will be performed."

    return msg


# ============================================
#                 erase_help
# ============================================
def erase_help() -> str:
    msg = "Performs a full chip erase on Mn using the st-flash utility provided by\n"
    msg += "the stlink tools repository: https://github.com/stlink-org/stlink.\n\n"
    msg += "<warning>NOTE</warning>: this command requires the use of a ST Link "
    msg += "hardware programmer connected directly to the Manage MCU. This command "
    msg += "will NOT work via just a USB connection.\nAdditionally, after performing "
    msg += "the erase operation, you will need to reset the device ID and find poles.\n"
    msg += "Additionally, if your device is an exo, you will need to perform a belt "
    msg += "calibration and calibrate the IMU. These functions are best performed "
    msg += "using Dephy's GUI, which you should have received access to with your "
    msg += "purchase.\n\n"
    msg += "<warning>NOTE</warning>: if your device is an exo, you will need to flash "
    msg += "Actpack firmware onto the device BEFORE finding poles. Once pole finding "
    msg += "is complete, you can then flash your desired firmware onto your device."

    return msg
