WEIGHT_PENALTY_PER_TON = 0.02


def weight_adjustment_factor(weight_tons: float) -> float:
    return 1 + weight_tons * WEIGHT_PENALTY_PER_TON