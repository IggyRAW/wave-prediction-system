import numpy as np

# 高気圧と低気圧の座標と強さ (中心気圧)
high_pressures = [
    {"coord": np.array([100, 200]), "strength": 1020},
    {"coord": np.array([150, 50]), "strength": 1025},
]

low_pressures = [
    {"coord": np.array([300, 400]), "strength": 995},
    {"coord": np.array([500, 100]), "strength": 990},
]

# 合成ベクトルの初期化
total_wind_vector = np.array([0.0, 0.0])

# 高気圧から低気圧への風向きベクトルを計算し、合成
for high in high_pressures:
    for low in low_pressures:
        # 高気圧から低気圧へのベクトルを計算
        wind_vector = low["coord"] - high["coord"]

        # 距離の逆数を重みとして風向きに影響を与える (距離が近いほど強い影響)
        distance = np.linalg.norm(wind_vector)
        weight = 1 / distance  # 距離に反比例した重み

        # 気圧差も影響を加味
        pressure_diff = high["strength"] - low["strength"]
        weighted_vector = wind_vector * weight * pressure_diff

        # 合成ベクトルに加算
        total_wind_vector += weighted_vector

# 最終的な風向きの角度を計算 (北を0度、東を90度)
angle = np.degrees(np.arctan2(total_wind_vector[1], total_wind_vector[0]))


# コリオリの力を加味 (北半球の場合)
def adjust_for_coriolis(angle, hemisphere="north"):
    if hemisphere == "north":
        angle -= 30  # コリオリの力で右に曲がる
    elif hemisphere == "south":
        angle += 30  # 南半球では左に曲がる
    return angle


# 北半球の風向きを調整
adjusted_angle = adjust_for_coriolis(angle, "north")

# 風向きを表示
print(
    f"Total Wind direction (adjusted for Coriolis effect): {adjusted_angle:.2f} degrees"
)
