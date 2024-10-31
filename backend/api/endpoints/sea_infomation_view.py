import csv
import os
from datetime import datetime
from logging import getLogger

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from api.schemas.sea_infomation import (
    DirectionsDict,
    SeaInfomation,
    WaveHeightDict,
    WaveHeightModel,
    WaveQualityDict,
    WaveQualityModel,
    reverseWaveHeightDict,
    reverseWaveQualityDict,
)
from config.config_manager import ConfigManager
from db.setting import session
from db.tbl_sea_infomation import tbl_sea_infomation

logger = getLogger(__name__)
config = ConfigManager()

router = APIRouter()


# region 初期遷移API
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


# endregion


# region 波高更新API
@router.post("/wave/info/wave_height/{id}")
def post_wave_height(id: int, waveHeight: WaveHeightModel):
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
        record.wave_height = reverseWaveHeightDict.get(
            waveHeight.wave_height, None
        )
        session.commit()
        session.refresh(record)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(e)
        raise Exception(e)


# endregion


# region 波質更新API
@router.post("/wave/info/wave_quality/{id}")
def post_wave_quality(id: int, waveQuality: WaveQualityModel):
    """
    波質更新API
    """
    try:
        logger.info(f"波高更新API：{post_wave_quality.__name__}")
        # 波質をDBへ格納
        record = session.query(tbl_sea_infomation).filter_by(id=id).first()
        if record is None:
            raise HTTPException(
                status_code=404, detail="Sea information not found"
            )
        record.wave_quality = reverseWaveQualityDict.get(
            waveQuality.wave_quality, None
        )
        session.commit()
        session.refresh(record)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(e)
        raise Exception(e)


# endregion


# region CSV出力API
@router.get("/sea/list/output/csv/")
def output_csv():
    """
    CSV出力API
    """
    try:
        logger.info(f"CSV出力API{output_csv.__name__}")
        sea_infomations = session.query(tbl_sea_infomation).all()

        # CSVファイルの作成
        file_name = (
            f"sea_information_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        )
        file_path = f"/tmp/{file_name}"
        if not os.path.exists(os.path.dirname(file_path)):
            os.mkdir(os.path.dirname(file_path))

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # ヘッダー行
            writer.writerow(
                [
                    "id",
                    "time",
                    "wind_direction",
                    "wind",
                    "wave_direction",
                    "coastal_waves",
                    "period",
                    "tide",
                    "wave_height",
                    "wave_quality",
                ]
            )

            # データ行
            for info in sea_infomations:
                writer.writerow(
                    [
                        info.id,
                        info.time,
                        info.wind_direction,
                        info.wind,
                        info.wave_direction,
                        info.coastal_waves,
                        info.period,
                        info.tide,
                        info.wave_height,
                        info.wave_quality,
                    ]
                )
        return FileResponse(
            path=file_path, filename=file_name, media_type="text/csv"
        )

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)
