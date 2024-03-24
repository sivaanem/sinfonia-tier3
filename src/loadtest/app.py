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
        config_path: str = typer.Option('src/loadtest/.cli.toml'),
):    
    config = Config(config_path)
    
    print(repr(config))
    proceed = typer.confirm('Proceed?')
    if not proceed:
        raise typer.Abort()
    
    print('\nStarting ...\n')
    
    # Create report folder for current session
    if config.c['cli']['is_report']:
        os.makedirs(config.c['report']['report_root_path'], exist_ok=True)
    
    # Execute loadtest at different RPS
    for rps_per_user in config.c['load']['rps_per_users']:
        num_users = config.c['load']['users']
        print(f'Running loadtest @ {rps_per_user * num_users * 10} req/sec ...')
        
        # Export locust config to file
        config.export_cli_to_toml('src/loadtest/.locust.toml', rps_per_user)
        
        # Spawn locust command thread and pipe output to foreground
        locust_args = config.to_locust_args(rps_per_user)
        locust_cmd = locust.__getitem__(locust_args)
        locust_cmd & plumbum.FG
        
        print('Done! 45-second cool down ...')
        for i in range(45, 0, -1):
            if i % 5 == 0:
                print(f"{i} ...", end="")
            time.sleep(1)
        print()
        

if __name__ == '__main__':
    app()
