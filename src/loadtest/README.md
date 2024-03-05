# Loadtest CLI

Loadtest CLI is loadtest framework to interact with the Sinfonia orchestration system.

## Interacting with Loadtest CLI

The loadtest is designed to be interacted via a CLI as follows,

```
poetry run loadtest
```

Add the ```--help``` option to see the available arguments.

## Configuration

A default configuraton is given in ```.cli.toml```. You can define your own and pass to the CLI via the ```--config_path``` argument, or modify the default one.

There are two types of configurations, CLI and Locust. The CLI configurations are mainly for job automations. As an on-going development project, available arguments for the CLI configs are subject to change. On the other hand, Locust configurations are directly passed to the Locust CLI, and can be referenced [at this link](https://docs.locust.io/en/2.24.0/configuration.html). Note that we are currently using Locust 2.24.0. The CLI and Locust configs can be found in the ```[cli]``` and ```[locust]``` tag in ```.cli.toml```.

## Common uses

There are two modes of operations, local and global. The local mode loads ```[cli.local]``` configs.

## How does it work

Loadtest CLI is an abstraction layer on top of Locust to handle custom actions. After the appropriate configurations are set up, Loadtest CLI spawns a thread running a Locust job with the neccessary arguments.


