import hmac
import hashlib


def generate_hmac(key: str, message: str, algorithm: str = "sha256") -> str:
    key = key.strip().encode("utf-8")
    message = message.strip().encode("utf-8")

    try:
        hash_func = getattr(hashlib, algorithm.lower())
    except AttributeError:
        return "Unsupported hashing algorithm"

    return hmac.new(key, message, hash_func).hexdigest()