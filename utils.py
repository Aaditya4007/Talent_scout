import re

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None

def calculate_experience_level(years):
    if years < 2:
        return "Junior"
    elif years < 5:
        return "Mid-level"
    elif years < 8:
        return "Senior"
    else:
        return "Lead"
