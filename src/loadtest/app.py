import toml

import typer
import plumbum
from dotenv import load_dotenv
from yarl import URL

from src.loadtest.env import Env


app = typer.Typer()


locust = plumbum.local['locust']


@app.command()
def loadtest(
        local_mode: bool = typer.Option(False, help='Run in local mode [default = False]'),
        config: str = typer.Option('src/loadtest/.conf.toml', help='Config file path [default \'src/loadtest/config\']')
):    
    cf = toml.load(config)
    
    if local_mode:
        ev = toml.load('src/loadtest/.local.env.toml')
    else:
        ev = toml.load('src/loadtest/.dev.env.toml')
    
    env = Env(**cf, **ev)
    print(repr(env))
    
    proceed = typer.confirm('Proceed?')
    if not proceed:
        raise typer.Abort()
    
    python3 = plumbum.local['python3']
    python3['src/loadtest']
    
    locust_cmd = locust.__getitem__(env.to_locust_args())
    
    # Execute command and move output to foreground
    locust_cmd & plumbum.FG
        

if __name__ == '__main__':
    app()
