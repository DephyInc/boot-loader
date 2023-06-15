from flexsea.utilities.constants import dephyPath


# ============================================
#              Path Configuration
# ============================================

# toolsDir is the name of the directory (mirrored on S3), whereas
# toolsPath is the full path to that directory on the local file system
toolsDir = "bootloader_tools"
toolsPath = dephyPath.joinpath(toolsDir)

# firmwareDir is the name of the directory (mirrored on S3), whereas
# firmwarePath is the full path to that directory on the local file system
firmwareDir = "firmware"
firmwarePath = dephyPath.joinpath(firmwareDir)


# ============================================
#              S3 Configuration
# ============================================

# Private bucket where the firmware is stored
dephyFirmwareBucket = "dephy-firmware-files"

# Credentials profile name
dephyAwsProfile = "dephy"


# ============================================
#                Dependencies
# ============================================
bootloaderTools = {
    "windows_64bit": {
        "bt121": [
            "bt121_image_tools.zip",
            "stm32flash.exe",
        ],
        "ex": [
            "psocbootloaderhost.exe",
        ],
        "habs": [
            "stm32_flash_loader.zip",
        ],
        "mn": [
            "DfuSeCommand.exe",
        ],
        "re": [
            "psocbootloaderhost.exe",
        ],
        "xbee": [
            "XB24C.zip",
        ],
    },
}


# ============================================
#                 Constants
# ============================================
firmwareExtensions = {"habs": "hex", "ex": "cyacd", "re": "cyacd", "mn": "dfu"}
targets = ["habs", "ex", "re", "bt121", "xbee", "mn"]
supportedOS = [
    "windows_64bit",
]


# ============================================
#                   Themes
# ============================================
themes = {
    "classic": {
        "info": {"fg": "blue", "options": []},
        "warning": {"fg": "yellow", "options": []},
        "error": {
            "fg": "red",
            "options": [
                "bold",
            ],
        },
        "success": {
            "fg": "green",
            "options": [
                "bold",
            ],
        },
    },
    "light": {
        "info": {"fg": "light_blue", "options": []},
        "warning": {"fg": "light_yellow", "options": []},
        "error": {
            "fg": "light_red",
            "options": [
                "bold",
            ],
        },
        "success": {
            "fg": "light_green",
            "options": [
                "bold",
            ],
        },
    },
    "dark": {
        "info": {
            "fg": "blue",
            "options": [
                "dark",
            ],
        },
        "warning": {
            "fg": "yellow",
            "options": [
                "dark",
            ],
        },
        "error": {
            "fg": "red",
            "options": [
                "dark",
                "bold",
            ],
        },
        "success": {
            "fg": "green",
            "options": [
                "dark",
                "bold",
            ],
        },
    },
    "default": {
        "info": {"fg": "default", "options": []},
        "warning": {"fg": "default", "options": []},
        "error": {"fg": "default", "options": []},
        "success": {"fg": "default", "options": []},
    },
}
