from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from utils import config
import uvicorn
import api
import web


class Application(FastAPI):
    def __init__(self, config: config.Config) -> None:
        super().__init__()

        self.mount("/static", StaticFiles(directory="static"), name="static")

        self.include_router(api.router)
        self.include_router(web.router)


if __name__ == '__main__':
    cfg: config.Config = config.load('./configs/dev.ini')

    app: Application = Application(cfg)

    uvicorn.run(
        app=app,
        host=cfg.app.host,
        port=cfg.app.port
    )