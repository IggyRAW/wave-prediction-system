from logging import getLogger

from fastapi import APIRouter, HTTPException, Query

from api.schemas.sea_infomation import (
    DirectionsDict,
    SeaInfomation,
    WaveHeight,
    WaveHeightDict,
    WaveQualityDict,
)
from config.config_manager import ConfigManager
from db.setting import session
from db.tbl_sea_infomation import tbl_sea_infomation

logger = getLogger(__name__)
config = ConfigManager()

router = APIRouter()


@router.get("/sea/info/list/")
def get_sea_infomation_list():
    """
    初期遷移
    """
    logger.info(get_sea_infomation_list.__name__)
    try:
        sea_infomations = session.query(tbl_sea_infomation).all()
        sea_infomations_list = [
            SeaInfomation(
                id=info.id,
                time=info.time,
                wind_direction=DirectionsDict[info.wind_direction],
                wind=info.wind,
                wave_direction=DirectionsDict[info.wave_direction],
                coastal_waves=info.coastal_waves,
                period=info.period,
                tide=info.tide,
                wave_height=WaveHeightDict.get(info.wave_height, None),
                wave_quality=WaveQualityDict.get(info.wave_quality, None),
            )
            for info in sea_infomations
        ]

        return sea_infomations_list
    except Exception as e:
        logger.error(e)
        raise Exception(e)


@router.post("/wave/info/wave_height/{id}")
def post_wave_height(id: int, waveHeight: WaveHeight):
    """
    波高更新API
    """
    try:
        logger.info(f"波高更新API：{post_wave_height.__name__}")
        # 波高をDBへ格納
        record = session.query(tbl_sea_infomation).filter_by(id=id).first()
        if record is None:
            raise HTTPException(
                status_code=404, detail="Sea information not found"
            )
        record.wave_height = waveHeight.wave_height
        session.commit()
        session.refresh(record)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(e)
        raise Exception(e)


@router.post("/wave/info/wave_quality/{id}")
def post_wave_quality(id: int, waveQuality: int = Query(..., ge=0)):
    """
    波高更新API
    """
    try:
        logger.info(f"波高更新API：{post_wave_quality.__name__}")
        # idとparamの確認
        if id < 0 or waveQuality < 0:
            raise ValueError("id or param must be a positive integer.")
        # 波質をDBへ格納
        record = session.query(tbl_sea_infomation).filter_by(id=id).first()
        if record is None:
            raise HTTPException(
                status_code=404, detail="Sea information not found"
            )
        record.wave_quality = waveQuality
        session.commit()
        session.refresh(record)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(e)
        raise Exception(e)
