def validate_affected_users(value):
    if type(value) is not int:
        raise TypeError("affected users must be an integer")
    if value < 1:
        raise ValueError("affected users must be greater than 0")

    return value

def validate_urgency(value):
    categories = ["low","medium","high"]

    if not isinstance(value, str):
        raise TypeError("urgency must be a string")

    valid_value = value.strip().lower()

    if valid_value not in categories:
        raise ValueError(f"please select from these options {categories}")
        
    return valid_value

