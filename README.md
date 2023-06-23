# FastAPI URL Shortener backend

This is a sample FastAPI + SQLAlchemy 2.0 project that I used for SQLite(aiosqlite) async tests.

## Getting Started
Steps to getting started:

* Install via `poetry install`.
* Activate shell `make env`
* Make migrations `make alembic_upgrade`
* Run the app locally `make start` or just `make` because (`.DEFAULT_GOAL` is `start`)
* Run linters `make lint`
* Run formatters `make format`
* Run test `pytest`
* Remove \_\_pycache\_\_$|\.pyc$|\.pyo$ `make clean`  
* Build image `make build`
* Run the app in the container `make run`
* Push image `make push` (with `git log --format="%h" -n 1` tag)
* Push image with `:latest` tag `make release`

To be able to push images to the docker registry, you need to do `docker login`,
see the [docs](https://docs.docker.com/engine/reference/commandline/login/).

