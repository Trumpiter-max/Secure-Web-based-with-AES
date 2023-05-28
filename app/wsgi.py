import os
from app import app

private_key_path = "/var/www/certificates/private_key.pem"
certificate_path = "/var/www/certificates/certificate.pem"

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True, threaded=True, ssl_context=('certificate.pem', 'private_key.pem'))