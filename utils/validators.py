def validate_numeric_input(value: str, min_val=None, max_val=None) -> float:
    """Validate and parse numeric input."""
    try:
        num = float(value)
        if min_val is not None and num < min_val:
            raise ValueError(f"Value must be at least {min_val}")
        if max_val is not None and num > max_val:
            raise ValueError(f"Value must be at most {max_val}")
        return num
    except ValueError:
        raise ValueError(f"'{value}' is not a valid number")
    
def validate_type(value: str, expected_type: type) -> bool:
    """Validate that the input value is of the expected type."""
    try:
        expected_type(value)
        return True
    except (ValueError, TypeError):
        return False