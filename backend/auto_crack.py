from hash_detector import detect_hash
from cracker import crack_hash


def auto_crack(hash_value):

    algorithm = detect_hash(hash_value)

    if algorithm is None:
        return {
            "algorithm": "unknown",
            "password": None
        }

    password = crack_hash(hash_value, algorithm)

    return {
        "algorithm": algorithm,
        "password": password
    }