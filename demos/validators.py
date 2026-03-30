

def validate_num(value):
    if isinstance(value, int) or isinstance(value, float):
        return value
    return None

def validate_string_value(value):
    if isinstance(value, str) and len(value) > 0:
        return value
    return None