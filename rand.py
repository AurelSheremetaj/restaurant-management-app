import random

def generate_4_digit_id(existing_ids=None):
    """
    Generate a unique 4-digit string ID.
    existing_ids: a set of existing IDs to avoid duplicates.
    """
    if existing_ids is None:
        existing_ids = set()
    while True:
        new_id = f"{random.randint(0, 9999):04d}"
        if new_id not in existing_ids:
            return new_id