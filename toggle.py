import argparse
import ctypes
import subprocess
import sys

import keyboard

if not ctypes.windll.shell32.IsUserAnAdmin():
    sys.exit("Script must be run as administrator.")


def toggle_vpn(tunnel_name: str, conf: str) -> None:
    svc = f"WireGuardTunnel${tunnel_name}"

    result = subprocess.run(
        ["sc", "query", "state=", "all"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if svc in result.stdout:
        subprocess.run(
            ["wireguard", "/uninstalltunnelservice", tunnel_name], check=True
        )
    else:
        subprocess.run(
            ["wireguard", "/installtunnelservice", conf],
            check=True,
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tunnel", help="Name of the WireGuard tunnel")
    parser.add_argument(
        "--config", help="Path to the WireGuard configuration file"
    )
    parser.add_argument("--hotkey", help="Keyboard shortcut to toggle VPN")

    args = parser.parse_args()

    if args.hotkey:
        keyboard.add_hotkey(
            args.hotkey, lambda: toggle_vpn(args.tunnel, args.config)
        )
        keyboard.wait()
    else:
        toggle_vpn(args.tunnel, args.config)


if __name__ == "__main__":
    main()
