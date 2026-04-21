from .base import *

# Producción usa JSON estructurado para CloudWatch/Datadog/etc.
LOGGING["handlers"]["console"]["formatter"] = "json"
# DisallowedHost se dispara por bots/scanners; silenciar el ruido
LOGGING["loggers"]["django.security.DisallowedHost"] = {
    "level": "ERROR",
    "handlers": ["console"],
    "propagate": False,
}

DEBUG = False
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL")
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
ADMINS = [env("DJANGO_ADMIN_EMAIL")]

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": env.str("AWS_STORAGE_BUCKET_NAME"),
            "region_name": env.str("AWS_S3_REGION_NAME", default="us-east-1"),
            "access_key": env.str("AWS_ACCESS_KEY_ID"),
            "secret_key": env.str("AWS_SECRET_ACCESS_KEY"),
            "querystring_auth": True,
            "signature_version": "s3v4",
            "default_acl": None,
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# WhiteNoise: cache de 1 año (el hash del manifest evita problemas de invalidación)
WHITENOISE_MAX_AGE = 60 * 60 * 24 * 365
WHITENOISE_INDEX_FILE = False
# Archivos ya comprimidos (no re-gzip)
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = (
    "jpg",
    "jpeg",
    "png",
    "gif",
    "webp",
    "zip",
    "gz",
    "br",
    "woff",
    "woff2",
)
