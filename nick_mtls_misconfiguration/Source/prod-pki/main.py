from fastapi import FastAPI, Query, Response
from fastapi.responses import PlainTextResponse, JSONResponse
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from datetime import datetime, timedelta
import time
import random

app = FastAPI()

CA_KEY_PATH = "ca.key"
CA_CERT_PATH = "ca.crt"
ALLOWLIST = {"user"}

# Predictable serial number counter (VULNERABLE!)
serial_counter = 1000

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
    return {"message": "Production PKI Server", "version": "2.1.0", "environment": "production"}

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/status")
def status():
    return {
        "server": "prod-pki",
        "uptime": random.randint(50000, 99999),
        "certificates_issued": random.randint(5000, 15000),
        "last_restart": "2024-01-01T00:00:00Z",
        "security_level": "high"
    }

@app.get("/metrics")
def metrics():
    return {
        "requests_total": random.randint(50000, 150000),
        "certificates_issued": random.randint(10000, 50000),
        "errors": random.randint(0, 5),
        "response_time_avg": random.uniform(0.05, 0.2),
        "security_events": random.randint(0, 3)
    }

@app.get("/info")
def info():
    return {
        "name": "Production PKI Server",
        "description": "Certificate Authority for production environment",
        "contact": "security-team@company.com",
        "documentation": "/docs",
        "security_policy": "strict"
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
            "/revoke - Revoke certificate",
            "/list - List issued certificates",
            "/config - Server configuration",
            "/audit - Audit logs",
            "/security - Security status"
        ]
    }

@app.get("/validate")
def validate_cert(cert_data: str = Query(...)):
    return {"valid": True, "reason": "Certificate validation completed", "security_checks": "passed"}

@app.get("/revoke")
def revoke_cert(serial: str = Query(...)):
    return {"revoked": True, "serial": serial, "timestamp": datetime.utcnow().isoformat(), "audit_logged": True}

@app.get("/list")
def list_certs():
    return {
        "certificates": [
            {"serial": "P123456", "subject": "CN=user", "issued": "2024-01-10", "status": "active"},
            {"serial": "P123457", "subject": "CN=service-account", "issued": "2024-01-12", "status": "active"},
            {"serial": "P123458", "subject": "CN=monitoring", "issued": "2024-01-14", "status": "active"}
        ],
        "total_issued": 3,
        "restricted_users": ["admin", "root", "system"],
        "note": "Admin certificates must be issued from dev environment"
    }

@app.get("/config")
def config():
    return {
        "ca_subject": str(ca_cert.subject),
        "ca_issuer": str(ca_cert.issuer),
        "validity_period": "365 days",
        "key_size": "2048 bits",
        "signature_algorithm": "SHA256",
        "environment": "production",
        "backup_pki": "dev-pki:8000", 
        "serial_number_policy": "sequential"
    }

@app.get("/ping")
def ping():
    return {"message": "pong", "timestamp": time.time()}

@app.get("/version")
def version():
    return {"version": "2.1.0", "build": "prod-2024-01-01"}

@app.get("/stats")
def stats():
    return {
        "total_requests": random.randint(100000, 500000),
        "successful_issues": random.randint(50000, 200000),
        "failed_requests": random.randint(0, 10),
        "average_response_time": random.uniform(0.02, 0.15),
        "security_events": random.randint(0, 5)
    }

@app.get("/debug")
def debug():
    return {
        "debug_mode": False,
        "log_level": "INFO",
        "environment": "production",
        "features": ["certificate_issuance", "validation", "revocation", "audit_logging"],
        "serial_number_policy": "sequential",
        "security_notes": [
            "Using sequential serial numbers for easier tracking",
            "Serial numbers increment by 1 for each certificate",
            "Current serial counter: " + str(serial_counter)
        ]
    }

@app.get("/audit")
def audit():
    return {
        "recent_events": [
            {"timestamp": "2024-01-15T10:30:00Z", "event": "certificate_issued", "user": "user", "ip": "192.168.1.100"},
            {"timestamp": "2024-01-15T10:25:00Z", "event": "certificate_validated", "user": "service-account", "ip": "10.0.0.50"},
            {"timestamp": "2024-01-15T10:20:00Z", "event": "access_denied", "user": "admin", "ip": "172.16.0.25", "reason": "not_in_allowlist"}
        ]
    }

@app.get("/security")
def security():
    return {
        "threat_level": "low",
        "recent_incidents": 0,
        "security_checks": "all_passed",
        "compliance_status": "compliant",
        "firewall_rules": [
            {"rule": "allow_internal_only", "status": "active"},
            {"rule": "block_external_admin", "status": "active"},
            {"rule": "rate_limit_requests", "status": "active"}
        ],
        "last_security_scan": "2024-01-15T09:00:00Z"
    }

@app.get("/api/v1/certificates")
def api_certificates():
    return {"certificates": [], "total": 0, "security_level": "high"}

@app.get("/api/v1/status")
def api_status():
    return {
        "status": "operational", 
        "environment": "production", 
        "security": "enabled",
        "load_balancer": "nginx:443"
    }

@app.get("/api/v2/health")
def api_v2_health():
    return {"status": "healthy", "version": "2.1.0"}

@app.get("/issue", response_class=PlainTextResponse)
def issue_cert(username: str = Query(...)):
    if username not in ALLOWLIST:
        return Response(content="Username not allowed", status_code=403)
    user_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
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
    return Response(content="Not currently supported, still in testing", status_code=501)