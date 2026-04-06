# HTTPS Setup Guide

This guide explains how to set up HTTPS for both local development and production deployment.

## Local Development (Self-Signed Certificate)

### Step 1: Generate SSL Certificate

#### On Windows (PowerShell):
```powershell
.\generate-ssl-cert.ps1
```

#### On Linux/Mac (Bash):
```bash
chmod +x generate-ssl-cert.sh
./generate-ssl-cert.sh
```

#### Manual Generation (if scripts don't work):
```bash
# Create ssl directory
mkdir -p nginx/ssl

# Generate certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/localhost.key \
  -out nginx/ssl/localhost.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/OU=IT/CN=localhost"
```

### Step 2: Start Services with Nginx
```bash
docker-compose down
docker-compose up -d --build
```

### Step 3: Trust the Certificate

#### Chrome/Edge (Windows):
1. Navigate to `https://localhost`
2. Click "Advanced" or "Not secure"
3. Click "Proceed to localhost (unsafe)" or "Continue to site"
4. Or import certificate:
   - Open Chrome Settings → Privacy and security → Security → Manage certificates
   - Import `nginx/ssl/localhost.crt` to "Trusted Root Certification Authorities"

#### Firefox:
1. Navigate to `https://localhost`
2. Click "Advanced"
3. Click "Accept the Risk and Continue"
4. Or go to Settings → Privacy & Security → Certificates → View Certificates → Import

#### Safari (Mac):
1. Double-click `nginx/ssl/localhost.crt`
2. Add to Keychain
3. Open Keychain Access
4. Find the certificate and set to "Always Trust"

### Step 4: Access Your Application
```
https://localhost
```

The application will now be accessible via HTTPS!

## Production Deployment

### Option 1: Let's Encrypt (Free SSL Certificate)

#### Install Certbot
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx
```

#### Generate Certificate
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

#### Update docker-compose.prod.yml
```yaml
nginx:
  volumes:
    - /etc/letsencrypt:/etc/letsencrypt:ro
```

#### Update nginx.conf for Production
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # ... rest of configuration
}
```

#### Auto-Renewal
```bash
# Test renewal
sudo certbot renew --dry-run

# Add to crontab for auto-renewal
sudo crontab -e
# Add this line:
0 0 * * * certbot renew --quiet
```

### Option 2: Custom SSL Certificate

If you have a purchased SSL certificate:

1. **Copy certificate files to nginx/ssl/**
   ```bash
   cp your-certificate.crt nginx/ssl/
   cp your-private-key.key nginx/ssl/
   cp your-ca-bundle.crt nginx/ssl/  # if applicable
   ```

2. **Update nginx.conf**
   ```nginx
   ssl_certificate /etc/nginx/ssl/your-certificate.crt;
   ssl_certificate_key /etc/nginx/ssl/your-private-key.key;
   ```

3. **Restart Nginx**
   ```bash
   docker-compose restart nginx
   ```

### Option 3: Cloudflare SSL (Easiest for Production)

1. **Add your domain to Cloudflare**
2. **Update nameservers** to Cloudflare's
3. **Enable SSL/TLS** in Cloudflare dashboard
4. **Set SSL mode to "Full" or "Full (strict)"**
5. **Use Cloudflare Origin Certificate** in your nginx config

## Django Settings for HTTPS

Update `backend/config/settings.py` for production:

```python
# HTTPS Settings
SECURE_SSL_REDIRECT = True  # Redirect HTTP to HTTPS
SESSION_COOKIE_SECURE = True  # Send cookies only over HTTPS
CSRF_COOKIE_SECURE = True  # Send CSRF cookie only over HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Additional security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

## Nginx SSL Best Practices

### Strong SSL Configuration
```nginx
# Modern SSL configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
ssl_prefer_server_ciphers off;

# SSL session cache
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;
```

## Testing SSL Configuration

### Online Tools
- **SSL Labs**: https://www.ssllabs.com/ssltest/
- **SSL Checker**: https://www.sslshopper.com/ssl-checker.html

### Command Line
```bash
# Test SSL connection
openssl s_client -connect localhost:443 -servername localhost

# Check certificate details
openssl x509 -in nginx/ssl/localhost.crt -text -noout

# Test with curl
curl -v https://localhost
```

## Troubleshooting

### Certificate Not Trusted
- Import the certificate to your system's trusted certificates
- Use browser's "Proceed anyway" option for development
- For production, use a certificate from a trusted CA

### ERR_CERT_AUTHORITY_INVALID
- Normal for self-signed certificates in development
- Click "Advanced" and proceed
- Or import certificate to trusted store

### Mixed Content Warnings
- Ensure all resources (CSS, JS, images) are loaded via HTTPS
- Update Django settings: `SECURE_PROXY_SSL_HEADER`
- Check for hardcoded HTTP URLs in templates

### Nginx Won't Start
```bash
# Check nginx configuration
docker-compose exec nginx nginx -t

# Check logs
docker-compose logs nginx

# Verify certificate files exist
ls -la nginx/ssl/
```

### Certificate Expired
```bash
# For Let's Encrypt
sudo certbot renew

# For self-signed (regenerate)
./generate-ssl-cert.sh
docker-compose restart nginx
```

## Security Checklist

- [ ] Use strong SSL protocols (TLSv1.2+)
- [ ] Enable HSTS
- [ ] Set secure cookie flags
- [ ] Implement CSP headers
- [ ] Regular certificate renewal
- [ ] Monitor SSL expiration
- [ ] Use strong ciphers
- [ ] Enable OCSP stapling
- [ ] Redirect HTTP to HTTPS
- [ ] Test with SSL Labs

## Certificate Renewal

### Let's Encrypt (Auto-renewal)
```bash
# Test renewal
certbot renew --dry-run

# Manual renewal
certbot renew

# Restart nginx after renewal
docker-compose restart nginx
```

### Self-Signed (Development)
```bash
# Regenerate certificate
./generate-ssl-cert.sh

# Restart services
docker-compose restart nginx
```

## Production Deployment Checklist

1. [ ] Obtain valid SSL certificate (Let's Encrypt or purchased)
2. [ ] Update nginx.conf with production domain
3. [ ] Configure Django HTTPS settings
4. [ ] Set up certificate auto-renewal
5. [ ] Test SSL configuration with SSL Labs
6. [ ] Enable HSTS
7. [ ] Update ALLOWED_HOSTS in Django
8. [ ] Configure firewall (allow 80, 443)
9. [ ] Set up monitoring for certificate expiration
10. [ ] Document certificate renewal process

## Quick Commands Reference

```bash
# Generate self-signed certificate
./generate-ssl-cert.sh

# Start with HTTPS
docker-compose up -d

# Check nginx config
docker-compose exec nginx nginx -t

# Reload nginx
docker-compose exec nginx nginx -s reload

# View certificate details
openssl x509 -in nginx/ssl/localhost.crt -text -noout

# Test HTTPS connection
curl -k https://localhost

# Check SSL Labs rating (production)
# Visit: https://www.ssllabs.com/ssltest/
```

## Support

For issues:
1. Check nginx logs: `docker-compose logs nginx`
2. Verify certificate files exist in `nginx/ssl/`
3. Test nginx config: `docker-compose exec nginx nginx -t`
4. Check Django logs for HTTPS-related errors
5. Review browser console for mixed content warnings

Your application is now ready for secure HTTPS deployment! 🔒
