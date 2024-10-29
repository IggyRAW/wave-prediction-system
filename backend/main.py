from contextlib import asynccontextmanager
from logging import getLogger

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from api.endpoints.get_wave_quality import router as get_wave_quality_router
from api.endpoints.get_weathar import get_weathar_data
from api.endpoints.get_weathar import router as get_weathar_router
from config.config_manager import ConfigManager
from manager.log_manager import initLogger

initLogger(__file__)
logger = getLogger(__name__)

config = ConfigManager()


scheduler = BackgroundScheduler()


# API起動時にスケジューラも起動
@asynccontextmanager
async def lifespan(app: FastAPI):
    # スケジューラ起動(毎朝5時に実行)
    scheduler.add_job(get_weathar_data, CronTrigger(minute=55, hour="5-18"))
    # scheduler.add_job(get_weathar_data, "interval", seconds=10)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(title=config.get_project("project_name"), lifespan=lifespan)

# ルーターの登録
app.include_router(get_weathar_router)
app.include_router(get_wave_quality_router)


@app.exception_handler(Exception)
async def conflict_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "detail": str(exc)},
    )


def main():
    uvicorn.run(app, host="0.0.0.0", port=config.get_project("id"))


if __name__ == "__main__":
    try:
        logger.info("=====Start API=====")
        main()

    except Exception as e:
        print(f"エラーが発生しました: {e}")
