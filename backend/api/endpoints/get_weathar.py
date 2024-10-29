import os
import re
from datetime import datetime
from logging import getLogger

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, WebSocket

from config.config_manager import ConfigManager
from db.setting import session
from db.tbl_sea_infomation import tbl_sea_infomation

WindDirection = {
    "N": "北",
    "NNE": "北北東",
    "NE": "北東",
    "ENE": "東北東",
    "E": "東",
    "ESE": "東南東",
    "SE": "南東",
    "SSE": "南南東",
    "S": "南",
    "SSW": "南南西",
    "SW": "南西",
    "WSW": "西南西",
    "W": "西",
    "WNW": "西北西",
    "NW": "北西",
    "NNW": "北北西",
}
WaveDirection = {
    "n": "北",
    "nne": "北北東",
    "ne": "北東",
    "ene": "東北東",
    "e": "東",
    "ese": "東南東",
    "se": "南東",
    "sse": "南南東",
    "s": "南",
    "ssw": "南南西",
    "sw": "南西",
    "wsw": "西南西",
    "w": "西",
    "wnw": "西北西",
    "nw": "北西",
    "nnw": "北北西",
}

logger = getLogger(__name__)

config = ConfigManager()

router = APIRouter()

URL = config.get_path("wethar_url")
ORIGIN_DATA_PATH = config.get_path("origin_data_path")
WAVE_DATA_PATH = config.get_path("wave_data_path")
MODEL_CSV_PATH = config.get_path("model_csv_path")


@router.websocket("/weather/")
async def get_weathar(websocket: WebSocket):
    """
    気象情報から波情報をスクレイピング
    """
    logger.info("気象情報から波情報をスクレイピング")

    await websocket.accept()
    try:
        result = requests.get(URL)
        result.raise_for_status()

        soup = BeautifulSoup(result.text, "html.parser")

        # データを抽出（例としてテーブルの行を取得）
        data = []
        wave_data = []
        table = soup.find("table", class_="hour_yohou")
        rows = table.find_all("tr")

        for i, row in enumerate(rows):
            await websocket.send_text(f"Progress: {(i+1)/len(rows)*100}%")
            # 最初はスルー
            if rows[0] == row:
                continue

            cols = row.find_all("td")
            # 時間
            hour = int(cols[0].text.strip())
            now = datetime.now()
            time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            time = time.strftime("%Y/%m/%d %H:%M")

            # 風向
            wind_direction_classname = cols[4].find("span").get("class")[1]
            result = re.search(r"_([^_]+)_png", wind_direction_classname)
            wind_direction = WindDirection[result.group(1)]

            # 風
            wind = cols[4].text.strip().replace("m", "")

            # 波向
            if len(cols) != 6:
                wave_direction_img = os.path.basename(
                    cols[5].find("img").get("src")
                )
                result = re.search(r"_([^_]+).png", wave_direction_img)
                wave_direction = WaveDirection[result.group(1)]

                # 沿岸波浪
                wave = cols[5].text.strip()
                pattern = r"([0-9.]+)\s*m\s*.*?([0-9.]+)\s*秒"
                matchs = re.search(pattern, wave)
                if matchs:
                    wave_height = matchs.group(1)
                    wave_period = matchs.group(2)

                # 潮汐
                tide = cols[6].text.strip().replace("㎝", "")
            else:
                # 潮汐
                tide = cols[5].text.strip().replace("㎝", "")

            # DBに格納
            sea_infomation = tbl_sea_infomation(
                time=time,
                wind_direction=wind_direction,
                wind=float(wind),
                wave_direction=wave_direction,
                coastal_waves=float(wave_height),
                period=float(wave_period),
                tide=int(tide),
            )
            session.add(sea_infomation)

            wave_condition = tbl_wave_conditions(
                time=time, wave_height=0, wave_quality=0
            )
            session.add(wave_condition)

            data.append(
                [
                    time,
                    wind_direction,
                    float(wind),
                    wave_direction,
                    float(wave_height),
                    float(wave_period),
                    int(tide),
                ]
            )
            wave_data.append([time, 0, 0])

        # データカラムの設定
        conditions_df = pd.DataFrame(data)
        conditions_df.columns = [
            "時間",
            "風向",
            "風",
            "波向",
            "沿岸波浪",
            "周期",
            "潮汐",
        ]

        wave_conditions_df = pd.DataFrame(wave_data)
        wave_conditions_df.columns = ["時間", "波高", "波質"]

        # 既存CSVファイルに書き込み
        conditions_df.to_csv(
            ORIGIN_DATA_PATH, mode="a", header=False, index=False
        )
        wave_conditions_df.to_csv(
            WAVE_DATA_PATH, mode="a", header=False, index=False
        )

        # モデル投入用CSVの生成
        create_wave_conditions_csv()

        logger.info("csvを出力しました。")

        await websocket.send_text("Complete")

    finally:
        await websocket.close()


def get_weathar_data():
    """
    気象情報から波情報をスクレイピング
    """
    logger.info("気象情報から波情報をスクレイピング")

    try:
        result = requests.get(URL)
        result.raise_for_status()

        soup = BeautifulSoup(result.text, "html.parser")

        # データを抽出（例としてテーブルの行を取得）
        table = soup.find("table", class_="hour_yohou")
        rows = table.find_all("tr")

        ll = rows[1]
        cols = ll.find_all("td")
        hour = int(cols[0].text.strip())
        now = datetime.now()
        time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
        time = time.strftime("%Y/%m/%d %H:%M")

        # 風向
        wind_direction_classname = cols[4].find("span").get("class")[1]
        result = re.search(r"_([^_]+)_png", wind_direction_classname)
        wind_direction = WindDirection[result.group(1)]

        # 風
        wind = cols[4].text.strip().replace("m", "")

        # 波向
        wave_direction_img = os.path.basename(cols[5].find("img").get("src"))
        result = re.search(r"_([^_]+).png", wave_direction_img)
        wave_direction = WaveDirection[result.group(1)]

        # 沿岸波浪
        wave = cols[5].text.strip()
        pattern = r"([0-9.]+)\s*m\s*.*?([0-9.]+)\s*秒"
        matchs = re.search(pattern, wave)
        if matchs:
            wave_height = matchs.group(1)
            wave_period = matchs.group(2)
        else:
            wave_height = 0
            wave_period = 0

        # 潮汐
        tide = cols[6].text.strip().replace("㎝", "")

        # DBに格納
        sea_infomation = tbl_sea_infomation(
            time=time,
            wind_direction=wind_direction,
            wind=float(wind),
            wave_direction=wave_direction,
            coastal_waves=float(wave_height),
            period=float(wave_period),
            tide=int(tide),
        )
        session.add(sea_infomation)
        session.commit()

    except Exception as e:
        logger.error(e)
        raise Exception(e)

    # for row in rows:
    #     # 最初はスルー
    #     if rows[0] == row:
    #         continue

    #     cols = row.find_all("td")
    #     # 時間
    #     hour = int(cols[0].text.strip())
    #     now = datetime.now()
    #     time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
    #     time = time.strftime("%Y/%m/%d %H:%M")

    #     # 風向
    #     wind_direction_classname = cols[4].find("span").get("class")[1]
    #     result = re.search(r"_([^_]+)_png", wind_direction_classname)
    #     wind_direction = WindDirection[result.group(1)]

    #     # 風
    #     wind = cols[4].text.strip().replace("m", "")

    #     # 波向
    #     if len(cols) != 6:
    #         wave_direction_img = os.path.basename(
    #             cols[5].find("img").get("src")
    #         )
    #         result = re.search(r"_([^_]+).png", wave_direction_img)
    #         wave_direction = WaveDirection[result.group(1)]

    #         # 沿岸波浪
    #         wave = cols[5].text.strip()
    #         pattern = r"([0-9.]+)\s*m\s*.*?([0-9.]+)\s*秒"
    #         matchs = re.search(pattern, wave)
    #         if matchs:
    #             wave_height = matchs.group(1)
    #             wave_period = matchs.group(2)

    #         # 潮汐
    #         tide = cols[6].text.strip().replace("㎝", "")
    #     else:
    #         # 潮汐
    #         tide = cols[5].text.strip().replace("㎝", "")

    #     # DBに格納
    #     sea_infomation = tbl_sea_infomation(
    #         time=time,
    #         wind_direction=wind_direction,
    #         wind=float(wind),
    #         wave_direction=wave_direction,
    #         coastal_waves=float(wave_height),
    #         period=float(wave_period),
    #         tide=int(tide),
    #     )
    #     session.add(sea_infomation)
    #     session.commit()
    #     data.append(
    #         [
    #             time,
    #             wind_direction,
    #             float(wind),
    #             wave_direction,
    #             float(wave_height),
    #             float(wave_period),
    #             int(tide),
    #         ]
    #     )
    #     wave_data.append([time, 0, 0])

    # # データカラムの設定
    # conditions_df = pd.DataFrame(data)
    # conditions_df.columns = [
    #     "時間",
    #     "風向",
    #     "風",
    #     "波向",
    #     "沿岸波浪",
    #     "周期",
    #     "潮汐",
    # ]

    # wave_conditions_df = pd.DataFrame(wave_data)
    # wave_conditions_df.columns = ["時間", "波高", "波質"]

    # # 既存CSVファイルに書き込み
    # conditions_df.to_csv(ORIGIN_DATA_PATH, mode="a", header=False, index=False)
    # wave_conditions_df.to_csv(
    #     WAVE_DATA_PATH, mode="a", header=False, index=False
    # )

    # # モデル投入用CSVの生成
    # create_wave_conditions_csv()

    # logger.info("csvを出力しました。")


def create_wave_conditions_csv():
    """
    モデル投入用CSV作成関数
    """
    conditions_df = pd.read_csv(ORIGIN_DATA_PATH)
    wave_conditions_df = pd.read_csv(WAVE_DATA_PATH)

    # データフレームの結合
    df = pd.merge(conditions_df, wave_conditions_df, on="時間", how="inner")
    df.to_csv(MODEL_CSV_PATH, index=False)
