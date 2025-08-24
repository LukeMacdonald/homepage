import os
from datetime import UTC, datetime

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID

CERT_DIR = "/etc/ssl/certs"


def get_cert_details():
    files = os.listdir(CERT_DIR)
    certificates = [f"{CERT_DIR}/{c}" for c in files if c.endswith(".crt")]

    for path in certificates:
        with open(path, "rb") as f:
            cert_data = f.read()

        try:
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        except ValueError:
            continue  # skip non-PEM certs

        cn = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        return {
            "File Name": os.path.basename(path),
            "Common Name": cn,
            "Issuer:": cert.issuer.rfc4514_string(),
            "Serial:": cert.serial_number,
            "Valid From:": cert.not_valid_before_utc,
            "Valid Until:": cert.not_valid_after_utc,
            "Expired:": cert.not_valid_after_utc < datetime.now(UTC),
        }
