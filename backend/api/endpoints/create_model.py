import os
from logging import getLogger

import joblib
import numpy as np
from fastapi import APIRouter, WebSocket
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from config.config_manager import ConfigManager
from exceptions.base import LibraryError
from exceptions.file import FileNotFoundError
from utils import load_csv

logger = getLogger(__name__)

config = ConfigManager()
ENCODER_WIND_DIRECTION_PATH = config.get_path("encoder_wind_direction_path")
ENCODER_WAVE_DORECTION_PATH = config.get_path("encoder_wave_direction_path")
SCALER_PATH = config.get_path("scaler_path")
WAVE_HEIGHT_MODEL_PATH = config.get_path("wave_height_model_path")
WAVE_QUALITY_MODEL_PATH = config.get_path("wave_quality_model_path")
DATA_PATH = config.get_path("data_path")

router = APIRouter()


@router.websocket("/create_model/")
async def create_model(websocket: WebSocket):
    await websocket.accept()
    try:
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(DATA_PATH)

        # データ読み込み
        df = load_csv(DATA_PATH)

        X = df[["風向", "風", "波向", "沿岸波浪", "周期", "潮汐"]]

        # 正解データ（波高と波質）
        y_wave_height = df["波高"]
        y_wave_quality = df["波質"]

        # カテゴリカルデータをOne-Hotエンコーディング
        encoder_wind_direction = OneHotEncoder(sparse_output=False)
        encoded_wind_direction = encoder_wind_direction.fit_transform(
            X[["風向"]]
        )
        encoder_wave_direction = OneHotEncoder(sparse_output=False)
        encoded_wave_direction = encoder_wave_direction.fit_transform(
            X[["波向"]]
        )

        # スケーリング
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(
            X[["風", "沿岸波浪", "周期", "潮汐"]]
        )

        # # 特徴量の結合
        X_processed = np.hstack(
            [encoded_wind_direction, encoded_wave_direction, scaled_features]
        )

        # 分類モデル（波高の予測）
        wave_height_model = RandomForestClassifier()
        wave_height_model.fit(X_processed, y_wave_height)

        # 分類モデル（波質の予測）
        wave_quality_model = RandomForestClassifier()
        wave_quality_model.fit(X_processed, y_wave_quality)

        # モデルを保存する
        joblib.dump(wave_height_model, WAVE_HEIGHT_MODEL_PATH)
        joblib.dump(wave_quality_model, WAVE_QUALITY_MODEL_PATH)
        joblib.dump(encoder_wind_direction, ENCODER_WIND_DIRECTION_PATH)
        joblib.dump(encoder_wave_direction, ENCODER_WAVE_DORECTION_PATH)
        joblib.dump(scaler, SCALER_PATH)

        logger.info("Successful Model creation!!")

    except LibraryError as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)

    finally:
        await websocket.close()
