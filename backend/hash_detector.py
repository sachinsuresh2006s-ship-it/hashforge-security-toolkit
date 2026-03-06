import re

def detect_hash(hash_value):

    hash_value = hash_value.strip()

    if re.fullmatch(r"[a-fA-F0-9]{32}", hash_value):
        return "md5"

    elif re.fullmatch(r"[a-fA-F0-9]{40}", hash_value):
        return "sha1"

    elif re.fullmatch(r"[a-fA-F0-9]{64}", hash_value):
        return "sha256"

    elif re.fullmatch(r"[a-fA-F0-9]{128}", hash_value):
        return "sha512"

    else:
        return None