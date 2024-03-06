import time

import typer
import plumbum
from dotenv import load_dotenv
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
    
    # Export locust config to file
    config.export_cli_to_toml('src/loadtest/.locust.toml')
    
    # Spawn locust command thread and pipe output to foreground
    locust_cmd & plumbum.FG
        

if __name__ == '__main__':
    app()
