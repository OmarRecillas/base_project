from .production import *

LOGGING["handlers"]["console"]["formatter"] = "json"

DEBUG = False
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["uat.tu-dominio.com"])

SECURE_HSTS_SECONDS = 60

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL", default="uat@tu-dominio.com")

LOGGING["root"]["level"] = "INFO"
