import random
import string

def generate_account_number(user_id=None):
    """Generate a random account number"""
    digits = ''.join(random.choices(string.digits, k=10))
    return f"ACCT-{digits}"