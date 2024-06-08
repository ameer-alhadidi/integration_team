from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec
import os

app = FastAPI()

# Configure the upload directory
UPLOAD_DIRECTORY = "uploads"

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

def get_attribute_value(name, oid):
    try:
        return name.get_attributes_for_oid(oid)[0].value
    except IndexError:
        return None

@app.post("/upload-certificate")
async def upload_certificate(certificate: UploadFile = File(...)):
    try:
        # Read the certificate file contents
        certificate_data = await certificate.read()

        # Save the certificate file to the upload directory
        file_path = os.path.join(UPLOAD_DIRECTORY, certificate.filename)
        with open(file_path, "wb") as file:
            file.write(certificate_data)

        # Load the certificate using cryptography library
        cert = x509.load_pem_x509_certificate(certificate_data, default_backend())

        # Extract certificate information
        subject = cert.subject
        issuer = cert.issuer
        serial_number = cert.serial_number
        not_before = cert.not_valid_before
        not_after = cert.not_valid_after

        # Extract public key information
        public_key = cert.public_key()
        if isinstance(public_key, rsa.RSAPublicKey):
            public_key_algorithm = "RSA"
            public_key_size = public_key.key_size
        elif isinstance(public_key, ec.EllipticCurvePublicKey):
            public_key_algorithm = "EC"
            public_key_size = public_key.curve.key_size
        else:
            public_key_algorithm = "Unknown"
            public_key_size = None

        # Extract extensions
        extensions = cert.extensions
        subject_alternative_names = []
        extended_key_usage = []
        for ext in extensions:
            if isinstance(ext.value, x509.SubjectAlternativeName):
                subject_alternative_names = [str(name) for name in ext.value]
            elif isinstance(ext.value, x509.ExtendedKeyUsage):
                extended_key_usage = [oid.dotted_string for oid in ext.value]

        # Create a response with the extracted certificate information
        response_data = {
            "filename": certificate.filename,
            "subject": {
                "common_name": get_attribute_value(subject, x509.NameOID.COMMON_NAME),
                "organization": get_attribute_value(subject, x509.NameOID.ORGANIZATION_NAME),
                "organizational_unit": get_attribute_value(subject, x509.NameOID.ORGANIZATIONAL_UNIT_NAME),
                "locality": get_attribute_value(subject, x509.NameOID.LOCALITY_NAME),
                "state_or_province": get_attribute_value(subject, x509.NameOID.STATE_OR_PROVINCE_NAME),
                "country": get_attribute_value(subject, x509.NameOID.COUNTRY_NAME),
            },
            "issuer": {
                "common_name": get_attribute_value(issuer, x509.NameOID.COMMON_NAME),
                "organization": get_attribute_value(issuer, x509.NameOID.ORGANIZATION_NAME),
                "organizational_unit": get_attribute_value(issuer, x509.NameOID.ORGANIZATIONAL_UNIT_NAME),
                "locality": get_attribute_value(issuer, x509.NameOID.LOCALITY_NAME),
                "state_or_province": get_attribute_value(issuer, x509.NameOID.STATE_OR_PROVINCE_NAME),
                "country": get_attribute_value(issuer, x509.NameOID.COUNTRY_NAME),
            },
            "serial_number": str(serial_number),
            "not_before": not_before.isoformat(),
            "not_after": not_after.isoformat(),
            "fingerprint_sha1": cert.fingerprint(hashes.SHA1()).hex(),
            "fingerprint_sha256": cert.fingerprint(hashes.SHA256()).hex(),
            "public_key": {
                "algorithm": public_key_algorithm,
                "key_size": public_key_size,
            },
            "subject_alternative_names": subject_alternative_names,
            "extended_key_usage": extended_key_usage,
        }

        return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

# Add Swagger metadata to the file upload parameter
upload_certificate.__doc__ = """
    Upload a certificate file.

    - **certificate**: The certificate file to upload.
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)