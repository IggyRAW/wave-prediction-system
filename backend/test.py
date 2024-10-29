import numpy as np
import pandas as pd
import joblib
from config.config_manager import ConfigManager
from utils import load_csv, WaveHeight, WaveQuality


config = ConfigManager()
ENCODER_WIND_DIRECTION_PATH = config.get_path("encoder_wind_direction_path")
ENCODER_WAVE_DORECTION_PATH = config.get_path("encoder_wave_direction_path")
SCALER_PATH = config.get_path("scaler_path")
WAVE_HEIGHT_MODEL_PATH = config.get_path("wave_height_model_path")
WAVE_QUALITY_MODEL_PATH = config.get_path("wave_quality_model_path")
DATA_PATH = config.get_path("data_path")
TEST_DATA = config.get_path("test_data_path")

# データ読み込み
df = load_csv(TEST_DATA)

# エンコーダーとスケーラーの読み込み
encoder_wind_direction = joblib.load(ENCODER_WIND_DIRECTION_PATH)
encoder_wave_direction = joblib.load(ENCODER_WAVE_DORECTION_PATH)
scaler = joblib.load(SCALER_PATH)

# モデルをロード
wave_height_model = joblib.load(WAVE_HEIGHT_MODEL_PATH)
wave_quality_model = joblib.load(WAVE_QUALITY_MODEL_PATH)

# 前処理の適用
encoded_wind_direction = encoder_wind_direction.transform(df[["風向"]])
encoded_wave_direction = encoder_wave_direction.transform(df[["波向"]])
scaled_features = scaler.transform(df[["風", "沿岸波浪", "周期", "潮汐"]])

# 特徴量の結合
X = pd.concat(
    [
        pd.DataFrame(encoded_wind_direction),
        pd.DataFrame(encoded_wave_direction),
        pd.DataFrame(scaled_features),
    ],
    axis=1,
)

# 波高の予想
predicted_wave_height = wave_height_model.predict(X)
print(f"波高予測：{WaveHeight[predicted_wave_height[0]]}")

# 波質の予測
predicted_wave_quality = wave_quality_model.predict(X)
print(f"波質予測：{WaveQuality[predicted_wave_quality[0]]}")
