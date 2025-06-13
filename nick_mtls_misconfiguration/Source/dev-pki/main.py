from fastapi import FastAPI, Query, Response
from fastapi.responses import PlainTextResponse, JSONResponse
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from datetime import datetime, timedelta
import os
import time
import random

app = FastAPI()

CA_KEY_PATH = "ca.key"
CA_CERT_PATH = "ca.crt"

with open(CA_KEY_PATH, "rb") as f:
    ca_key = load_pem_private_key(f.read(), password=None)
with open(CA_CERT_PATH, "rb") as f:
    ca_cert = x509.load_pem_x509_certificate(f.read())

def generate_rsa_key():
    """Generate an RSA key"""
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=None
    )

@app.get("/")
def root():
    return {"message": "Dev PKI Server", "version": "1.0.0", "environment": "development"}

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/status")
def status():
    return {
        "server": "dev-pki",
        "uptime": random.randint(1000, 9999),
        "certificates_issued": random.randint(50, 200),
        "last_restart": "2024-01-15T10:30:00Z"
    }

@app.get("/metrics")
def metrics():
    return {
        "requests_total": random.randint(1000, 5000),
        "certificates_issued": random.randint(100, 500),
        "errors": random.randint(0, 10),
        "response_time_avg": random.uniform(0.1, 0.5)
    }

@app.get("/info")
def info():
    return {
        "name": "Development PKI Server",
        "description": "Certificate Authority for development environment",
        "contact": "dev-team@company.com",
        "documentation": "/docs"
    }

@app.get("/docs")
def docs():
    return {
        "endpoints": [
            "/health - Health check",
            "/status - Server status",
            "/metrics - Performance metrics",
            "/info - Server information",
            "/validate - Validate certificate",
            "/check-username - Check if username is allowed",
            "/revoke - Revoke certificate",
            "/list - List issued certificates",
            "/config - Server configuration"
        ]
    }

@app.get("/validate")
def validate_cert(cert_data: str = Query(...)):
    return {"valid": random.choice([True, False]), "reason": "Certificate validation completed"}

@app.get("/check-username")
def check_username(username: str = Query(...)):
    """Check if a username is allowed for certificate issuance"""
    restricted_users = ["root", "system", "service"]
    if username.lower() in restricted_users:
        return {"allowed": False, "reason": "Username is restricted"}
    elif username.lower() == "admin":
        return {"allowed": False, "reason": "Admin certificates require special approval"}
    else:
        return {"allowed": True, "reason": "Username is permitted"}

@app.get("/revoke")
def revoke_cert(serial: str = Query(...)):
    return {"revoked": True, "serial": serial, "timestamp": datetime.utcnow().isoformat()}

@app.get("/list")
def list_certs():
    return {
        "certificates": [
            {"serial": "123456", "subject": "CN=test-user", "issued": "2024-01-10"},
            {"serial": "123457", "subject": "CN=guest", "issued": "2024-01-12"},
            {"serial": "123458", "subject": "CN=developer", "issued": "2024-01-14"}
        ]
    }

@app.get("/config")
def config():
    return {
        "ca_subject": str(ca_cert.subject),
        "ca_issuer": str(ca_cert.issuer),
        "validity_period": "365 days",
        "key_size": "2048 bits",
        "signature_algorithm": "SHA256",
        "restricted_users": ["root", "system", "service"],
        "environment": "development",
        "debug_mode": True,
        "note": "This server is for development only - admin certs allowed for testing",
        "warning": "Using weak RSA key generation for testing purposes"
    }

@app.get("/ping")
def ping():
    return {"message": "pong", "timestamp": time.time()}

@app.get("/version")
def version():
    return {"version": "1.0.0", "build": "dev-2024-01-15"}

@app.get("/stats")
def stats():
    return {
        "total_requests": random.randint(5000, 15000),
        "successful_issues": random.randint(200, 800),
        "failed_requests": random.randint(0, 20),
        "average_response_time": random.uniform(0.05, 0.3)
    }

@app.get("/debug")
def debug():
    return {
        "debug_mode": True,
        "log_level": "DEBUG",
        "environment": "development",
        "features": ["certificate_issuance", "validation", "revocation"],
        "recent_denials": [
            {"timestamp": "2024-01-15T09:30:00Z", "username": "admin", "reason": "Admin certificates require special approval"},
            {"timestamp": "2024-01-15T09:25:00Z", "username": "root", "reason": "Username is restricted"}
        ],
        "security_notes": [
            "Weak RSA key generation enabled for testing",
            "Small key sizes used for faster generation",
            "Predictable parameters for debugging"
        ]
    }

@app.get("/api/v1/certificates")
def api_certificates():
    return {"certificates": [], "total": 0}

@app.get("/api/v1/status")
def api_status():
    return {
        "status": "operational", 
        "environment": "development",
        "features": ["certificate_issuance", "intermediate_ca_issuance"],
        "peer": "prod-pki:8000",
        "note": "Development server - more permissive policies",
        "security_warning": "Using weak cryptography for testing"
    }

@app.get("/issue", response_class=PlainTextResponse)
def issue_cert(username: str = Query(...)):
    # Check if username is in restricted list (but allow admin for dev purposes)
    restricted_users = ["root", "system", "service"]
    if username.lower() in restricted_users:
        return Response(content="Username not allowed", status_code=403)
    
    user_key = generate_rsa_key()
    subject = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, username),
    ])
    csr = x509.CertificateSigningRequestBuilder().subject_name(subject).sign(user_key, hashes.SHA256())
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(user_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .sign(ca_key, hashes.SHA256())
    )
    cert_pem = cert.public_bytes(serialization.Encoding.PEM)
    key_pem = user_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return Response(content=key_pem + cert_pem, media_type="text/plain")

@app.get("/issue-ca", response_class=PlainTextResponse)
def issue_intermediate_ca(username: str = Query(...)):
    """Issue an intermediate CA certificate - WARNING: This is for advanced users only!"""
    intermediate_key = generate_rsa_key()
    subject = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, f"{username} Intermediate CA"),
    ])
    
    # Create intermediate CA certificate
    intermediate_cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(intermediate_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=1),
            critical=True,
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=True,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .sign(ca_key, hashes.SHA256())
    )
    
    cert_pem = intermediate_cert.public_bytes(serialization.Encoding.PEM)
    key_pem = intermediate_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    
    return Response(content=key_pem + cert_pem, media_type="text/plain") 