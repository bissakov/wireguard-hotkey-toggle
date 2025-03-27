import argparse
import ctypes
import logging
import subprocess
import sys

import keyboard

if not ctypes.windll.shell32.IsUserAnAdmin():
    sys.exit("Script must be run as administrator.")


def setup_logger(verbose: bool) -> logging.Logger:
    logger = logging.getLogger("VPNToggle")
    logger.setLevel(logging.DEBUG if verbose else logging.CRITICAL)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler("vpn_toggle.log", mode="a")
    file_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def is_torrent_running(logger: logging.Logger) -> bool:
    try:
        result = subprocess.run(
            ["tasklist", "/fi", "IMAGENAME eq qbittorrent.exe"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        out = result.stdout
        return "No tasks" not in out
    except subprocess.CalledProcessError as e:
        logger.error(f"Error checking torrent status: {e}")
        return False


def toggle_vpn(
    tunnel_name: str, conf: str, logger: logging.Logger, check_torrent: bool
) -> None:
    svc = f"WireGuardTunnel${tunnel_name}"

    try:
        result = subprocess.run(
            ["sc", "query", "state=", "all"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        logger.debug("Successfully retrieved service status.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error querying services: {e}")
        return

    if svc in result.stdout:
        try:
            subprocess.run(
                ["wireguard", "/uninstalltunnelservice", tunnel_name],
                check=True,
            )
            logger.info("VPN tunnel service uninstalled successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error uninstalling VPN tunnel: {e}")
    else:
        if check_torrent and is_torrent_running(logger):
            ctypes.windll.user32.MessageBoxW(
                0,
                "Close torrent application before turning on VPN!",
                "Error",
                0x10,
            )
            return

        try:
            subprocess.run(
                ["wireguard", "/installtunnelservice", conf],
                check=True,
            )
            logger.info("VPN tunnel service installed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error installing VPN tunnel: {e}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging to console and file",
    )
    parser.add_argument("--tunnel", help="Name of the WireGuard tunnel")
    parser.add_argument(
        "--config", help="Path to the WireGuard configuration file"
    )
    parser.add_argument("--hotkey", help="Keyboard shortcut to toggle VPN")
    parser.add_argument(
        "--torrent_check",
        action="store_true",
        help="Disable torrent check before turning on VPN",
    )

    args = parser.parse_args()

    logger = setup_logger(args.verbose)
    logger.info("VPN toggle script started.")

    if args.verbose:
        logger.info("Verbose mode ON.")
    else:
        logger.info("Verbose mode OFF.")

    if args.torrent_check:
        logger.info("Torrent process check ON.")
    else:
        logger.info("Torrent process check OFF.")

    try:
        if args.hotkey:
            logger.info(f"Setting up hotkey: {args.hotkey}")
            keyboard.add_hotkey(
                args.hotkey,
                lambda: toggle_vpn(
                    args.tunnel, args.config, logger, args.torrent_check
                ),
            )
            logger.info("Hotkey registered; waiting for key press...")
            keyboard.wait()
        else:
            toggle_vpn(args.tunnel, args.config, logger, args.torrent_check)
    except KeyboardInterrupt:
        logger.info("Shutdown requested... Exiting gracefully.")
        sys.exit(0)
    except (Exception, BaseException) as e:
        logger.exception(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
