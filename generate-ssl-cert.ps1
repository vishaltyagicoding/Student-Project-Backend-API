# PowerShell script to generate self-signed SSL certificate for Windows
# Run this script to create SSL certificates for localhost

Write-Host "Generating self-signed SSL certificate for localhost..." -ForegroundColor Green

# Create ssl directory if it doesn't exist
$sslDir = "nginx\ssl"
if (-not (Test-Path $sslDir)) {
    New-Item -ItemType Directory -Path $sslDir -Force | Out-Null
}

# Check if OpenSSL is available
$opensslPath = Get-Command openssl -ErrorAction SilentlyContinue

if ($opensslPath) {
    # Use OpenSSL if available
    Write-Host "Using OpenSSL to generate certificate..." -ForegroundColor Yellow
    
    & openssl req -x509 -nodes -days 365 -newkey rsa:2048 `
        -keyout "$sslDir\localhost.key" `
        -out "$sslDir\localhost.crt" `
        -subj "/C=US/ST=State/L=City/O=Organization/OU=IT/CN=localhost" `
        -addext "subjectAltName=DNS:localhost,DNS:*.localhost,IP:127.0.0.1"
    
    Write-Host "SSL certificate generated successfully using OpenSSL!" -ForegroundColor Green
} else {
    # Use PowerShell's New-SelfSignedCertificate
    Write-Host "Using PowerShell to generate certificate..." -ForegroundColor Yellow
    
    $cert = New-SelfSignedCertificate `
        -DnsName "localhost", "127.0.0.1" `
        -CertStoreLocation "Cert:\CurrentUser\My" `
        -NotAfter (Get-Date).AddYears(1) `
        -KeyAlgorithm RSA `
        -KeyLength 2048
    
    # Export certificate
    $certPath = "$sslDir\localhost.crt"
    $keyPath = "$sslDir\localhost.key"
    $pfxPath = "$sslDir\localhost.pfx"
    $password = ConvertTo-SecureString -String "localhost" -Force -AsPlainText
    
    # Export to PFX
    Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $password | Out-Null
    
    # Export certificate (public key)
    Export-Certificate -Cert $cert -FilePath $certPath -Type CERT | Out-Null
    
    # Convert PFX to PEM format for private key (requires OpenSSL)
    Write-Host "Note: Private key export requires OpenSSL. Install OpenSSL or use the certificate from Windows Certificate Store." -ForegroundColor Yellow
    
    Write-Host "SSL certificate generated successfully using PowerShell!" -ForegroundColor Green
    Write-Host "Certificate thumbprint: $($cert.Thumbprint)" -ForegroundColor Cyan
}

Write-Host "`nCertificate files:" -ForegroundColor Green
Write-Host "  Certificate: $sslDir\localhost.crt" -ForegroundColor Cyan
Write-Host "  Private Key: $sslDir\localhost.key" -ForegroundColor Cyan
Write-Host "`nNote: You may need to trust this certificate in your browser." -ForegroundColor Yellow
