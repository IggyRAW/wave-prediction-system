import sys

from sqlalchemy import TEXT, Column, Float, Integer

from db.setting import Base, engine


class tbl_sea_infomation(Base):
    """
    ユーザモデル
    """

    __tablename__ = "tbl_sea_infomation"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    time = Column("time", TEXT)
    wind_direction = Column("wind_direction", TEXT)
    wind = Column("wind", Float)
    wave_direction = Column("wave_direction", TEXT)
    coastal_waves = Column("coastal_waves", Float)
    period = Column("period", Float)
    tide = Column("tide", Integer)
    wave_height = Column("wave_height", TEXT)
    wave_quality = Column("wave_quality", TEXT)


def main(args):
    """
    メイン関数
    """
    Base.metadata_create_all(bind=engine)


if __name__ == "__main__":
    main(sys.args)
