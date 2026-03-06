import hashlib
import base64
import re


def clean_text(text: str) -> str:
    return text.strip()


# ---------------- HASH FUNCTIONS ---------------- #

def md5_hash(text: str) -> str:
    return hashlib.md5(clean_text(text).encode()).hexdigest()


def sha1_hash(text: str) -> str:
    return hashlib.sha1(clean_text(text).encode()).hexdigest()


def sha256_hash(text: str) -> str:
    return hashlib.sha256(clean_text(text).encode()).hexdigest()


def sha512_hash(text: str) -> str:
    return hashlib.sha512(clean_text(text).encode()).hexdigest()


# ---------------- BASE64 ---------------- #

def base64_encode(text: str) -> str:
    encoded = base64.b64encode(clean_text(text).encode())
    return encoded.decode()


def base64_decode(text: str) -> str:
    try:
        decoded = base64.b64decode(clean_text(text), validate=True)
        return decoded.decode()
    except Exception:
        return "Invalid Base64 input"


# ---------------- HEX ---------------- #

def hex_encode(text: str) -> str:
    return clean_text(text).encode().hex()


def hex_decode(text: str) -> str:
    try:
        decoded = bytes.fromhex(clean_text(text))
        return decoded.decode()
    except Exception:
        return "Invalid Hex input"


# ---------------- HASH IDENTIFIER ---------------- #

def identify_hash(hash_string: str) -> str:
    """
    Identify hash type using length + hex validation
    """

    hash_string = clean_text(hash_string)

    if re.fullmatch(r"[a-fA-F0-9]{32}", hash_string):
        return "MD5"

    elif re.fullmatch(r"[a-fA-F0-9]{40}", hash_string):
        return "SHA1"

    elif re.fullmatch(r"[a-fA-F0-9]{64}", hash_string):
        return "SHA256"

    elif re.fullmatch(r"[a-fA-F0-9]{128}", hash_string):
        return "SHA512"

    else:
        return "Unknown"