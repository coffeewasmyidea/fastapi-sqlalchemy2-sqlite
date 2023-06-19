import uvicorn
import multiprocessing


APP_NAME = "app.main:app"

APP_HOST = "0.0.0.0"

APP_PORT = 8080

LOG_LEVEL = "info"

DEBUG = True


def number_of_workers() -> int:
    return 1 if DEBUG else (multiprocessing.cpu_count() * 2) + 1


if __name__ == "__main__":
    options = {
        "app": APP_NAME,
        "host": APP_HOST,
        "port": APP_PORT,
        "workers": number_of_workers(),
        "reload": DEBUG,
        "log_level": LOG_LEVEL,
    }

    uvicorn.run(**options)
