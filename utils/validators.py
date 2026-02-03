def validate_numeric_input(value: str, min_val: float = None, max_val: float = None) -> float:
    '''
    Validate and parse numeric input
    
    :param value: input value
    :type value: str
    :param min_val: minimum value
    :type min_val: float
    :param max_val: maximum value
    :type max_val: float
    :return: value in float type
    :rtype: float
    '''
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
    '''
    Validate that the input value is of the expected type
    
    :param value: input value
    :type value: str
    :param expected_type: expected type
    :type expected_type: type
    :return: True if same type else False
    :rtype: bool
    '''
    try:
        expected_type(value)
        return True
    except (ValueError, TypeError):
        return False