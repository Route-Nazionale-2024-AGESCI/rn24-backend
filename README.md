# RN24 backend

Django backoffice and API backend for the mobile app

# How to contribute

Open this folder in [VSCode](https://code.visualstudio.com/) and the [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers) will be detected.


Just click on "Reopen in Container" and you will have a fully working environment with the correct extensions and linters.

We use [ruff](https://github.com/astral-sh/ruff), [black](https://github.com/psf/black) and [pre-commit](https://pre-commit.com/).

Both development and deploy is done with Docker and a compose file.

Install Docker on your machine and check that it's working running

`docker run hello-world`

copy the template file for env variables and change with appropiate values

`cp .env_dist .env`

run the local environment

`docker compose up`

now you should be able to visit http://localhost:8000 and see Django
