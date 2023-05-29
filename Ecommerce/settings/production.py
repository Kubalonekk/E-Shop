from .base import *


ALLOWED_HOSTS = ['kubalonek99.usermd.net', 'www.kubalonek99.usermd.net']


STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')



CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000 # 1 year
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
