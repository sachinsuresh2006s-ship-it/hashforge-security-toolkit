from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import hashing
import hmac_utils
import cracker
from auto_crack import auto_crack

import hashlib

app = FastAPI(title="HashForge Security Toolkit", version="1.0")

# -----------------------------
# CORS Configuration
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Request Models
# -----------------------------

class HashRequest(BaseModel):
    text: str


class HmacRequest(BaseModel):
    key: str
    message: str


class CrackRequest(BaseModel):
    hash: str
    algorithm: str


class AutoCrackRequest(BaseModel):
    hash: str


# -----------------------------
# Root Endpoint
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "HashForge API running 🚀",
        "version": "1.0"
    }


# Prevent favicon error in logs
@app.get("/favicon.ico")
def favicon():
    return {}


# -----------------------------
# Hash Generation
# -----------------------------

@app.post("/hash/md5")
def md5(data: HashRequest):
    return {"hash": hashing.md5_hash(data.text)}


@app.post("/hash/sha1")
def sha1(data: HashRequest):
    return {"hash": hashing.sha1_hash(data.text)}


@app.post("/hash/sha256")
def sha256(data: HashRequest):
    return {"hash": hashing.sha256_hash(data.text)}


@app.post("/hash/sha512")
def sha512(data: HashRequest):
    return {"hash": hashing.sha512_hash(data.text)}


# -----------------------------
# Encoding / Decoding
# -----------------------------

@app.post("/encode/base64")
def encode_base64(data: HashRequest):
    return {"result": hashing.base64_encode(data.text)}


@app.post("/decode/base64")
def decode_base64(data: HashRequest):
    return {"result": hashing.base64_decode(data.text)}


@app.post("/encode/hex")
def encode_hex(data: HashRequest):
    return {"result": hashing.hex_encode(data.text)}


@app.post("/decode/hex")
def decode_hex(data: HashRequest):
    return {"result": hashing.hex_decode(data.text)}


# -----------------------------
# HMAC Generation
# -----------------------------

@app.post("/hmac")
def generate_hmac(data: HmacRequest):

    try:
        result = hmac_utils.generate_hmac(data.key, data.message)
        return {"hmac": result}

    except Exception:
        raise HTTPException(status_code=500, detail="HMAC generation failed")


# -----------------------------
# Hash Cracker
# -----------------------------

@app.post("/crack")
def crack(data: CrackRequest):

    try:
        password = cracker.crack_hash(data.hash, data.algorithm)

    except Exception:
        raise HTTPException(status_code=500, detail="Cracking failed")

    if password is None or password == "Not found in wordlist":
        raise HTTPException(status_code=404, detail="Password not found")

    return {
        "hash": data.hash,
        "algorithm": data.algorithm,
        "password": password
    }


# -----------------------------
# Auto Detect + Auto Crack
# -----------------------------

@app.post("/auto-crack")
def auto_crack_api(data: AutoCrackRequest):

    result = auto_crack(data.hash)

    if result["password"] is None or result["password"] == "Not found in wordlist":
        raise HTTPException(status_code=404, detail="Password not found")

    return result


# -----------------------------
# File Hashing
# -----------------------------

@app.post("/filehash")
async def file_hash(file: UploadFile = File(...)):

    try:
        content = await file.read()

        return {
            "filename": file.filename,
            "size_bytes": len(content),
            "md5": hashlib.md5(content).hexdigest(),
            "sha1": hashlib.sha1(content).hexdigest(),
            "sha256": hashlib.sha256(content).hexdigest(),
            "sha512": hashlib.sha512(content).hexdigest()
        }

    except Exception:
        raise HTTPException(status_code=500, detail="File hashing failed")