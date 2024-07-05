import base64

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

from rn24.settings import PRIVATE_KEY_PATH, PUBLIC_KEY_PATH


def sign_string(message_string):
    message_bytes = message_string.encode("utf-8")
    key = ECC.import_key(open(PRIVATE_KEY_PATH).read())
    h = SHA256.new(message_bytes)
    signer = DSS.new(key, "fips-186-3")
    signature = signer.sign(h)
    base64_signature = base64.b64encode(signature).decode("utf-8")
    return base64_signature


def verify_signature(message_string, signature_base64):
    message_bytes = message_string.encode("utf-8")
    signature = base64.b64decode(signature_base64)
    key = ECC.import_key(open(PUBLIC_KEY_PATH).read())
    h = SHA256.new(message_bytes)
    verifier = DSS.new(key, "fips-186-3")
    try:
        verifier.verify(h, signature)
        return True
    except ValueError:
        return False
