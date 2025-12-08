def round_number(x: float, decimals: int = 2) -> float:
    """Round a float to a specified number of decimal places."""
    try:
        return round(float(x), decimals)
    except (ValueError, TypeError, OverflowError):
        return x

def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp the value between min_val and max_val."""
    return max(min_val, min(max_val, value))