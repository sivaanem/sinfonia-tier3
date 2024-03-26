#
# Sinfonia
#
# deploy helm charts to a cloudlet kubernetes cluster for edge-native applications
#
# Copyright (c) 2022-2023 Carnegie Mellon University
#
# SPDX-License-Identifier: MIT
#

from __future__ import annotations

import time
import argparse
from io import StringIO
from typing import Sequence
from uuid import UUID

import typer
from requests.exceptions import HTTPError
from yarl import URL

from src.domain import format
from . import __version__
from .cloudlet_deployment import sinfonia_deploy, CloudletDeployment
from .local_deployment import sinfonia_runapp


APP_NAME_TO_UUID = {
    "helloworld": "00000000-0000-0000-0000-000000000000",
    "loadtest": "00000000-0000-0000-0000-000000000111"
}


UUID_TO_APP_NAME = {
    "00000000-0000-0000-0000-000000000111": "loadtest",
    "00000000-0000-0000-0000-000000000000": "helloworld",
}


cli = typer.Typer()


def app_name_to_uuid(value: str) -> UUID:
    uuid = APP_NAME_TO_UUID.get(value, value)
    return UUID(uuid)


def uuid_to_app_name(uuid: str | UUID) -> str:
    return UUID_TO_APP_NAME[str(uuid)]


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """parse those args"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config-debug",
        action="store_true",
        help="Create wireguard and resolv config in current directory",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Extra logging for debugging"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--qrcode",
        choices=["compact", "alt"],
        help="Generate QR code for wireguard-android",
    )
    parser.add_argument(
        "--zeroconf",
        action="store_true",
        help="Try to discover local Tier2 through MDNS",
    )
    parser.add_argument("tier1_url", metavar="tier1-url", type=URL)
    parser.add_argument("application_uuid", metavar="application-uuid", type=app_name_to_uuid)
    parser.add_argument("application", nargs=argparse.REMAINDER)
    return parser.parse_args(args)


def print_deployment_status(
        application_uuid: UUID,
        deployments: list[CloudletDeployment], 
        connected_deployment: CloudletDeployment
):
    deployment_hosts = []
    for d in deployments:
        for _, v in d.tunnel_config.peers.items():
            deployment_hosts.append(str(v.endpoint_host))
            
    connected_deployment_peers_data = list(connected_deployment.tunnel_config.peers.values())
    connected_deployment_host = str(connected_deployment_peers_data[0].endpoint_host)
    
    status_repr = format.str.bold(format.str.green(connected_deployment.status))
    connected_deployment_host_repr = format.str.bold(format.str.magenta(connected_deployment_host))
            
    print()
    print("DEPLOYMENT STATUS")
    print(f"  * Deployed app: {application_uuid} ({uuid_to_app_name(application_uuid)})")
    print(f"  * Deployment size: {len(deployments)}")
    print(f"  * Deployment hosts: {deployment_hosts}")
    print(f"  * Connection status: {status_repr}")
    print(f"  * Connected host IP: {connected_deployment_host_repr}")
    print(f"  * Application key: {connected_deployment.application_key}")
    print(f"  * Deployment name: {connected_deployment.deployment_name}")
    print()


@cli.command()
def sinfonia_tier3_loadtest(
        tier1_url: str = typer.Option("http://192.168.245.31:5000"),
        application_uuid: str = typer.Option("loadtest"),
        application: str = typer.Option("/bin/bash"),
        loadtest_config_path: str = typer.Option("src/sinfonia_tier3_loadtest/.cli.toml"),
        T: int = typer.Option(5, help="Number of samples"),
        config_debug: bool = typer.Option(False),
        debug: bool = typer.Option(False),
        zeroconf: bool = typer.Option(False),
) -> int:
    try:
        application_uuid = UUID(application_uuid)
    except Exception:
        try:
            application_uuid = app_name_to_uuid(application_uuid)
        except Exception as e:
            print(f"exception {e}")
            exit(1)
    
    for t in range(T):
        print()
        print(f"STARTING SAMPLE T = {t+1} (of {T})")
        print("========================================")
        print()
        
        # Request one or more backend deployments
        try:
            print("Deploying... ")
            deployments = sinfonia_deploy(URL(tier1_url), application_uuid, debug, zeroconf)
            print("Done!")
        except ConnectionError:
            print("failed to connect to sinfonia-tier1/-tier2")
            return 1
        except HTTPError as e:
            print(f'failed to deploy backend: "{e.response.text}"')
            return 1

        # Pick the best deployment (first returned for now...)    
        deployment_data = deployments[0]
        deployment_peers_data = list(deployment_data.tunnel_config.peers.values())
        deployment_host = str(deployment_peers_data[0].endpoint_host)
        # print(deployment_data.to_pretty_format())
        
        print_deployment_status(
            application_uuid,
            deployments,
            deployment_data
        )
        
        # This is to wait for loadtest app to completely terminate
        # Not ideal (and can bug), but this seems to work for now
        if t != 0:
            time.sleep(45)
        
        try:
            with format.str.ForeCyan():
                sinfonia_runapp(
                    deployment_data.deployment_name,
                    deployment_data.tunnel_config,
                    deployment_host,
                    loadtest_config_path,
                    application,
                    config_debug,
                )
        except Exception as e:
            print(f"exception: {e}")
            break


if __name__ == '__main__':
    cli()
