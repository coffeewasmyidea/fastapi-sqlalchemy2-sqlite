import multiprocessing

import uvicorn

from app.settings import settings


def number_of_workers() -> int:
    return 1 if settings.DEBUG else (multiprocessing.cpu_count() * 2) + 1


def app_run():
    options = {
        "app": settings.UVICORN_APP_NAME,
        "host": settings.APP_HOST,
        "port": settings.APP_PORT,
        "workers": number_of_workers(),
        "reload": settings.DEBUG,
        "log_level": settings.UVICORN_LOG_LEVEL,
        "timeout_graceful_shutdown": settings.UVICORN_GRACEFUL_SHUTDOWN,
    }

    uvicorn.run(**options)


if __name__ == "__main__":
    app_run()
