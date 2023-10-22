# mc-server-syncer
compresses and decompresses a Minecraft server so a self hosted server is not dependent on a single host.

## Setup

Copy all 3 scripts into your minecraft server folder. Create a folder `.sync` in your minecraft server folder.
This `.sync` folder must be synchronized using an external provider, e.g. Google Drive.

The folder may also reside in a different directory. If this is the case, adapt the `sync_dir` path in the
`mc.py` script to your custom directory. Note that if the directory is on another drive, the scripts must be executed
with admin rights.

Note that the script is only tested on Windows systems and probably only works on Windows. Also, to use the autostart
feature of the `start.py` script, a spigot server is required.

## Usage

Before starting the server, run `start.py`.
The script will automatically check if there is a more recent version of the server in the specified sync folder.
If it is, the script will ask if it should overwrite your local server with the more recent version.
If your local server is more recent, nothing will happen.

After stopping the server, run `zip.py`.
This will compress all necessary files and place them in the sync folder.