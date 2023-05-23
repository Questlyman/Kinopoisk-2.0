# bureau 1440 test task

## Installation

### Requirements

#### Without docker
To install requirements only for starting service
without docker you should install poetry first and then run this command
```shell
poetry install --no-dev
```

But if you also want to install linters and framework for tests, you should run this command:

```shell
poetry install
```

#### With docker

No requirements needed to run this service at docker, except for docker-compose.

### Environment variables

To run this project you should set up `.env` and `.env.docker-compose` files(there is an `*.example` file for each one of how to fill up these files).
As for first attempt to run, you can just copy `.env.example` to `.env` and `.env.docker-compose.example` to `.env.docker-compose`.


### Docker

To run this project at docker, you should run this command:

```shell
docker-compose -f docker/docker-compose.local.yaml -p bureau-1440-test-task up
```


## Appendix

There is some utilities at `Makefile` that you can use.
To see them and messages, that explains what each command do, you should run 
```shell
make help
```
