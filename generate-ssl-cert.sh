#!/bin/bash

# Generate self-signed SSL certificate for local development
# This script creates SSL certificates for localhost

echo "Generating self-signed SSL certificate for localhost..."

# Create ssl directory if it doesn't exist
mkdir -p nginx/ssl

# Generate private key and certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/localhost.key \
  -out nginx/ssl/localhost.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/OU=IT/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,DNS:*.localhost,IP:127.0.0.1"

echo "SSL certificate generated successfully!"
echo "Certificate: nginx/ssl/localhost.crt"
echo "Private Key: nginx/ssl/localhost.key"
