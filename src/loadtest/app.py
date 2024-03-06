import os
import time

import typer
import plumbum
from dotenv import load_dotenv
from pathlib import Path
from yarl import URL

from loadtest.config import Config


app = typer.Typer()


locust = plumbum.local['locust']


@app.command()
def loadtest(
        local: bool = typer.Option(False),
        dry_run: bool = typer.Option(False),
        config_path: str = typer.Option('src/loadtest/.cli.toml'),
):    
    config = Config(local, config_path)
    
    print(repr(config))
    proceed = typer.confirm('Proceed?')
    if not proceed:
        raise typer.Abort()
    
    locust_args = config.to_locust_args()
    locust_cmd = locust.__getitem__(config.to_locust_args())
    
    if dry_run:
        print(locust_args)
        return 
    
    print('\nStarting ...\n')
    time.sleep(1)
    
    # Add base timestamp for current session
    bts_unix = int(time.time())
    config.cli['bts_unix'] = bts_unix
    
    # Create report folder for current session
    report_root_path = config.cli['carbon_report_root_path']
    session_root_path = str(Path(report_root_path) / str(bts_unix))
    os.makedirs(session_root_path, exist_ok=False)
    config.cli['carbon_report_root_path'] = session_root_path
    
    # Execute loadtest at different RPS
    for rps_per_user in config.rps['rps_per_users']:
        num_users = config.locust['users']
        print(f'Running loadtest @ {rps_per_user * num_users} req/sec ...')
        
        # Export locust config to file
        config.export_cli_to_toml('src/loadtest/.locust.toml', rps_per_user)
    
        # Spawn locust command thread and pipe output to foreground
        locust_cmd & plumbum.FG
        

if __name__ == '__main__':
    app()
