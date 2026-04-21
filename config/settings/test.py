import tempfile
import warnings

from .base import *

# En tests silenciamos logs para no contaminar el output de pytest
LOGGING["root"]["level"] = "CRITICAL"
LOGGING["loggers"]["django"]["level"] = "CRITICAL"
LOGGING["loggers"]["apps"]["level"] = "CRITICAL"

DEBUG = False

# Hasher rápido: los tests no necesitan seguridad criptográfica
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Email en memoria (no I/O ni consola)
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Cache local en memoria
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

MEDIA_ROOT = tempfile.mkdtemp(prefix="bp_test_media_")

warnings.filterwarnings("ignore", category=RuntimeWarning, module="django.db.models.fields")
