from typing import List, Optional

from pydantic import BaseModel, Field

DirectionsDict = {
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

WaveHeightDict = {
    "over_head": "頭オーバー",
    "head": "頭",
    "shoulder": "肩",
    "chest": "胸",
    "stomach": "腹",
    "waist": "腰",
    "thigh": "腿",
    "knees": "膝",
    "calm": "フラット",
}

WaveQualityDict = {
    "great": "とても良い",
    "good": "良い",
    "bad": "悪い",
    "terrible": "とても悪い",
}

# 辞書を反転
reverseWaveHeightDict = {v: k for k, v in WaveHeightDict.items()}
reverseWaveQualityDict = {v: k for k, v in WaveQualityDict.items()}


class SeaInfomation(BaseModel):
    id: Optional[int] = Field(None, ge=0, description="ID")
    time: str = Field(..., description="時刻")
    wind_direction: Optional[str] = Field(None, description="風向")
    wind: Optional[float] = Field(None, description="風")
    wave_direction: Optional[str] = Field(None, description="波向")
    coastal_waves: Optional[float] = Field(None, description="沿岸波浪")
    period: Optional[float] = Field(None, ge=0, description="周期")
    tide: Optional[int] = Field(None, ge=0, description="潮汐")
    wave_height: Optional[str] = Field(None, description="波高")
    wave_quality: Optional[str] = Field(None, description="波質")


class WaveHeightModel(BaseModel):
    wave_height: Optional[str] = Field(None, description="波高")


class WaveQualityModel(BaseModel):
    wave_quality: Optional[str] = Field(None, description="波質")
