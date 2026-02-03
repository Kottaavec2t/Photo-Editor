def round_number(n: float, decimals: int = 2) -> float:
    '''
    Round a number to a specified number of decimal places
    
    :param n: a number
    :type n: float
    :param decimals: the numbers of decimals after the comma
    :type decimals: int
    :return: rounded number
    :rtype: float
    '''
    try:
        return round(float(n), decimals)
    except (ValueError, TypeError, OverflowError):
        return n

def clamp(n: float, min_val: float, max_val: float) -> float:
    '''
    Clamp the number between min_val and max_val
    
    :param n: a number
    :type n: float
    :param min_val: minimum value
    :type min_val: float
    :param max_val: maximum value
    :type max_val: float
    :return: n | min_val | max_val
    :rtype: float
    '''
    return max(min_val, min(max_val, n))