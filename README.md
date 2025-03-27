# WireGuard Tunnel Toggle

Create a custom hotkey that toggles WireGuard toggle on and off.

## Installation

Copy contents of toggle.py script to your local Windows PC and install the dependency.

```bat
pip install keyboard
```

or

```bat
git clone https://github.com/bissakov/wireguard-hotkey-toggle.git
cd wireguard-hotkey-toggle

python -m venv venv
venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r .\requirements.txt
```

## Usage

### Directly

Make sure to run the script with admin privileges.
[All available keyboard modifier names](https://github.com/boppreh/keyboard)

```bat
python toggle.py --tunnel tunnel_name --config "path/to/tunnel_name.conf" --hotkey "windows+c --torrent_check --verbose"
```

```
usage: toggle.py [-h] [--verbose] --tunnel TUNNEL --config CONFIG [--hotkey HOTKEY] [--torrent_check]

Toggle a WireGuard VPN tunnel with optional torrent application check.

options:
  -h, --help       show this help message and exit
  --verbose        Enable verbose logging to console and file
  --tunnel TUNNEL  Name of the WireGuard tunnel
  --config CONFIG  Path to the WireGuard configuration file
  --hotkey HOTKEY  Keyboard shortcut to toggle VPN
  --torrent_check  Enable torrent check before turning on VPN

If --torrent_check is not provided, the torrent check is skipped. The script requires administrative privileges.
```

### Using Windows Task Scheduler

1. Create Task
2. General tab - Give a name and tick privileges box
3. Triggers tab - Create a trigger, change trigger type, select a specific user and give it a delay (optional)
4. Actions tab - Create an action, choose a type, fill program and argument fields
5. Press OK

![Create Task](assets/scheduler_0.png)
![General tab - Give a name and tick privileges box](assets/scheduler_1.png)
![Triggers tab - Create a trigger, change trigger type, select a specific user and give it a delay (optional)](assets/scheduler_2.png)
![Actions tab - Create an action, choose a type, fill program and argument fields](assets/scheduler_3.png)
![Press OK](assets/scheduler_4.png)
