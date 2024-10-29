from typing import List, Optional

from pydantic import BaseModel, Field


class SeaInfomation(BaseModel):
    id: Optional[int] = Field(None, ge=0, description="ID")
    time: str = Field(..., description="時刻")
    wind_direction: Optional[str] = Field(None, description="風向")
    wind: Optional[float] = Field(None, description="風")
    wave_direction: Optional[str] = Field(None, description="波向")
    coastal_waves: Optional[float] = Field(None, description="沿岸波浪")
    period: Optional[float] = Field(None, ge=0, description="周期")
    tide: Optional[int] = Field(None, ge=0, description="潮汐")
    wave_height: Optional[int] = Field(None, description="波高")
    wave_quality: Optional[int] = Field(None, description="波質")
