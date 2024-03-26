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
        headless: bool = typer.Option(False),
        tier2_url: str = typer.Option("")
):    
    config = Config(config_path)
    if tier2_url:
        print(tier2_url)
        config.c["network"]["app_root_url"] = str(URL(tier2_url).with_port(30080) / "api" / "v1")
        config.c["network"]["tier2_root_url"] = str(URL(tier2_url).with_port(30051) / "api" / "v1")
    
    print(repr(config))
    
    if not headless:
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
        config.export_cli_to_toml('src/loadtest/.locust.autogen.toml', rps_per_user)
        
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
