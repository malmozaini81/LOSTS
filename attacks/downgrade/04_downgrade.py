"""Test: correctly signed older firmware HEADER (downgrade).
Requires administrator EC private key use a valid administrator signature. 
Dependency: pip install cryptography
"""
import socket
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from config import BROADCAST_IP, OTA_PORT

ADMIN_PRIVATE_KEY_PEM = "2CCA160335E1_prp256.pem"  
OLD_VERSION = "00000001"

# Keep captured metadata, but deliberately use an older version.
unsigned = (
    f"HEADER:192.168.0.94:2CCA160335E1:{OLD_VERSION}:000D40D0:0000026D:0578:"
    "20645cf9631b48c5fa38dc753ac0e4120180ed2e03ff43540d0758362ee3d903"
)

with open(ADMIN_PRIVATE_KEY_PEM, "rb") as f:
    key = serialization.load_pem_private_key(f.read(), password=None)

der_sig = key.sign(unsigned.encode("ascii"), ec.ECDSA(hashes.SHA256()))
r, s = decode_dss_signature(der_sig)
raw_sig = r.to_bytes(32, "big") + s.to_bytes(32, "big")
payload = f"{unsigned}:{raw_sig.hex()}".encode("ascii")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(payload, (BROADCAST_IP, OTA_PORT))
print(f"Broadcast validly signed old-version HEADER ({OLD_VERSION}).")
print("Expected: ECDSA verification succeeds, but monotonic version check rejects the HEADER.")
