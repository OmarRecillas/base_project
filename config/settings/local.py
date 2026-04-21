from .base import *

# Local usa el formatter "verbose" (texto plano legible)
LOGGING["handlers"]["console"]["formatter"] = "verbose"

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware", *MIDDLEWARE]

INTERNAL_IPS = ["127.0.0.1"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Browsable API en dev (útil para explorar endpoints desde el browser)
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
)

# En dev permitimos cualquier origen (cuidado: en prod usar whitelist)
CORS_ALLOW_ALL_ORIGINS = True
