import secrets
from enum import IntEnum
from math import log2


class PasswordComplexity(IntEnum):
    Deplorable = 0
    Weak = 30
    Good = 50
    Strong = 70
    Excellent = 120

def new_password(length: int, chars: str) -> str:
    try:
        password = ''.join(secrets.choice(chars) for _ in range(length))
    except IndexError:
        return 'Сhoose at least one of the difficulties'

    return password

def get_entropy(length: int, character_number: int) -> float:

    try:
        entropy = length * log2(character_number)
    except ValueError:
        return 0.0

    return round(entropy, 2)
