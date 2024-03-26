#
# Sinfonia
#
# deploy helm charts to a cloudlet kubernetes cluster for edge-native applications
#
# Copyright (c) 2021-2023 Carnegie Mellon University
#
# SPDX-License-Identifier: MIT
#

from __future__ import annotations

import time
import subprocess
import sys
from itertools import chain
from pathlib import Path
from shutil import which
from tempfile import TemporaryDirectory
from typing import Sequence

from wireguard4netns import create_wireguard_tunnel
from wireguard_tools import WireguardConfig


def unique_namespace_name(name: str) -> str:
    """Returns a name with only ascii lowercase letters.

    Deriving it from the deployment name helps during development to match the
    deployed kubenetes environment with the local namespace, but it is not
    functionally required.
    """
    # str.translate is probably faster, but we only do this once...
    return "".join(c for c in name.lower() if c.islower()) or "sinfonia"


def sudo_create_wireguard_tunnel(
    netns_pid: int, interface: str, config: WireguardConfig, tmpdir: Path
) -> None:
    """Try to bring up wireguard tunnel with sudo sinfonia_tier3_loadtest.root_helper"""
    sudo = which("sudo")
    assert sudo is not None

    wireguard_conf = tmpdir / "wg.conf"
    wireguard_conf.write_text(config.to_wgconfig())

    # create, configure and attach WireGuard interface
    subprocess.run(
        [
            sudo,
            sys.executable,
            "-m",
            "sinfonia_tier3.root_helper",
            str(netns_pid),
            interface,
            str(wireguard_conf.resolve()),
        ],
        check=True,
    )


def sinfonia_runapp(
    deployment_name: str,
    config: WireguardConfig,
    deployment_host: str,
    application: Sequence[str],
    config_debug: bool = False,
) -> int:
    """Run application in an isolated network namespace with wireguard tunnel"""
    with TemporaryDirectory() as temporary_directory:
        if config_debug:
            temporary_directory = "."
        tmpdir = Path(temporary_directory)

        resolv_conf = tmpdir / "resolv.conf"
        resolv_conf.write_text(config.to_resolvconf(opt_ndots=5))

        if config_debug:
            wireguard_conf = tmpdir / "wg.conf"
            wireguard_conf.write_text(config.to_wgconfig())
            return 0

        unshare = which("unshare")
        assert unshare is not None

        NS = unique_namespace_name(deployment_name)
        WG = f"wg-{NS}"[:15]

        # Running two processes pretty much in parallel here, the first one
        # creates a new network namespace and then waits for the wireguard
        # interface.
        # The second process runs as root and creates and configures the
        # wireguard interface and attaches it to the new network namespace.
        with subprocess.Popen(
            [
                unshare,
                "--user",
                "--map-root-user",
                "--net",
                "--mount",
                "--",
                sys.executable,
                "-m",
                "sinfonia_tier3.netns_helper",
                "--resolvconf",
                str(resolv_conf.resolve()),
            ]
            + list(
                chain.from_iterable(
                    ("--address", str(address)) for address in config.addresses
                )
            )
            + [WG]
            + list(application),
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE,
        ) as netns_proc:
            try:
                create_wireguard_tunnel(netns_proc.pid, WG, config, tmpdir)
            except (AssertionError, FileNotFoundError, subprocess.CalledProcessError):
                print("Failed to run wireguard-go, falling back to sudo root helper")
                try:
                    sudo_create_wireguard_tunnel(netns_proc.pid, WG, config, tmpdir)
                except (AssertionError, subprocess.CalledProcessError):
                    print("Failed to run sudo root helper")
                    netns_proc.kill()
                    
            loadtest_command = f"poetry run loadtest --headless --tier2-url=\"http://{deployment_host}\""
            netns_proc.stdin.write(loadtest_command.encode("utf-8"))
            netns_proc.stdin.write(b"\n") 
            netns_proc.stdin.flush() 
            
            for line in iter(netns_proc.stdout.readline, b''):
                print(line.decode().strip())
                    
            remaining_output = netns_proc.stdout.read()
            if remaining_output:
                print(remaining_output.decode().strip())
                
            loadtest_command = [
                which("poetry"),
                "run",
                "loadtest",
                "--headless",
                "--tier2-url",
                "\"http://{deployment_host}\""
                ]
            loadtest_proc = subprocess.run(
                loadtest_command,
                shell=True,
                check=True,
                capture_output=True,
                )
            
            for line in iter(loadtest_proc.stdout.readline, b''):
                print(line.decode().strip())
                    
            remaining_output = loadtest_proc.stdout.read()
            if remaining_output:
                print(remaining_output.decode().strip())
            
            # leaving the context will wait for the application to exit
    return 0
