import hashlib
import os

# Absolute path for rockyou.txt
BASE_DIR = os.path.dirname(__file__)
WORDLIST = os.path.join(BASE_DIR, "rockyou.txt")


def crack_hash(target_hash, algorithm):

    target_hash = target_hash.strip().lower()
    algorithm = algorithm.lower()

    # Map algorithms to hashlib functions
    hash_functions = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512
    }

    if algorithm not in hash_functions:
        return "Unsupported algorithm"

    hash_func = hash_functions[algorithm]

    try:
        with open(WORDLIST, "r", encoding="latin-1") as file:

            for word in file:
                word = word.strip()

                hashed = hash_func(word.encode()).hexdigest()

                if hashed == target_hash:
                    return word

        return "Not found in wordlist"

    except FileNotFoundError:
        return "rockyou.txt not found"