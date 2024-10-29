from typing import Optional
from pandas import DataFrame
import pandas as pd

# region 指標辞書
Direction = {
    "北": 1,
    "北北東": 2,
    "北東": 3,
    "東北東": 4,
    "東": 5,
    "東南東": 6,
    "南東": 7,
    "南南東": 8,
    "南": 9,
    "南南西": 10,
    "南西": 11,
    "西南西": 12,
    "西": 13,
    "西北西": 14,
    "北西": 15,
    "北北西": 16,
}
WaveHeight = {
    1: "頭オーバー",
    2: "頭",
    3: "肩",
    4: "胸",
    5: "腹",
    6: "腰",
    7: "腿",
    8: "膝",
    9: "フラット",
}
WaveQuality = {1: "とても良い", 2: "良い", 3: "悪い", 4: "とても悪い"}
# endregion


def load_csv(path: str) -> Optional[DataFrame]:
    """
    CSVをデータフレームに変換する関数

    :param path: 読み込むCSVファイルのパス
    :return: DataFrame もしくは None（エラー時）
    """
    try:
        df = pd.read_csv(path, sep=None, engine="python", encoding="utf-8")
        return df
    except UnicodeDecodeError:
        # エンコーディングがutf-8でない場合、エンコーディングを再試行する
        try:
            df = pd.read_csv(
                path, sep=None, engine="python", encoding="shift-jis"
            )
            return df
        except Exception as e:
            print(f"読み込みエラー: {e}")
            return None
    except pd.errors.ParserError:
        # パースエラーの場合、異なる区切り文字を試みる
        try:
            df = pd.read_csv(path, delimiter=";", engine="python")
            return df
        except Exception as e:
            print(f"パースエラー: {e}")
            return None
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None
