# Base Project

Plantilla base para proyectos Django con settings por entorno, testing, linting y CI listo para usar.

---

## Stack

- **Python** 3.14
- **Django** 6.0
- **PostgreSQL** 16+
- **Ruff** (lint + format)
- **pytest-django** + **factory-boy** (testing)
- **pre-commit** (git hooks)
- **pip-tools** (dependency management)

---

## Prerequisites

Asegúrate de tener instalado:

- Python 3.14 — verifica con `python --version`
- PostgreSQL 17 o superior — verifica con `psql --version`
- Git — verifica con `git --version`

---

## Quick start

```bash
# 1. Clonar y entrar al repo
git clone https://github.com/OmarRecillas/base_project.git BP
cd base_project

# 2. Crear y activar el entorno virtual
python -m venv .venv_bp
# Windows PowerShell:
.venv_bp\Scripts\Activate.ps1
# macOS/Linux:
source .venv_bp/bin/activate

# 3. Instalar dependencias de desarrollo
pip install pip-tools
pip-sync requirements/local.txt

# 4. Crear la base de datos en Postgres
psql -U postgres
# Dentro de psql:
# CREATE USER dakshina WITH PASSWORD '<tu-password>' CREATEDB;
# CREATE DATABASE bp_db OWNER dakshina;
# \q

# 5. Variables de entorno
cp .env.example .env
# Edita .env con tu SECRET_KEY y DATABASE_URL

# 6. Migraciones + superuser
python manage.py migrate
python manage.py createsuperuser

# 7. Instalar hooks de pre-commit
pre-commit install

# 8. Correr el servidor
python manage.py runserver
```

Abre http://localhost:8000/herdir/ → debería cargar el admin.

---

## Environment variables

Copia `.env.example` a `.env` y rellena los valores. Variables requeridas:

| Variable | Descripción | Ejemplo |
|---|---|---|
| `DJANGO_SECRET_KEY` | Clave secreta de Django. Generar con: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` | `e!k%...` |
| `DJANGO_DEBUG` | Activa el debug mode (solo local). | `True` |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos, separados por coma. | `localhost,127.0.0.1` |
| `DATABASE_URL` | Conexión a Postgres. | `postgres://dakshina:pass@localhost:5432/bp_db` |
| `DJANGO_DEFAULT_FROM_EMAIL` | Email por defecto para envíos. | `no-reply@example.com` |
| `DJANGO_ADMIN_EMAIL` | Email que recibe alertas de errores 500 en prod. | `admin@example.com` |

---

## Project structure

```text
base_project/
├── apps/                    # Django apps del dominio
│   ├── core/                # Modelo base (BaseModel con UUID, timestamps)
│   └── users/               # User custom (email como username, profile_picture)
├── config/                  # Config global del proyecto
│   ├── settings/            # Settings split por entorno
│   │   ├── base.py          # Compartido entre todos los entornos
│   │   ├── local.py         # Desarrollo local
│   │   ├── test.py          # Tests (MD5 hasher, email in-memory)
│   │   ├── uat.py           # QA/staging
│   │   └── production.py    # Producción
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── requirements/            # Dependencias con pip-tools
│   ├── base.in              # Runtime común
│   ├── local.in             # Dev tools (ruff, pytest, pre-commit)
│   ├── uat.in
│   ├── production.in        # Gunicorn, whitenoise, sentry
│   └── *.txt                # Lockfiles generados (con hashes)
├── conftest.py              # Fixtures globales de pytest
├── manage.py
├── pyproject.toml           # Config de Ruff, pytest, coverage
├── .pre-commit-config.yaml  # Hooks de git
├── .env.example             # Plantilla de variables de entorno
└── README.md
```

---

## Settings per environment

Cada entorno hereda de `base.py` y sobrescribe lo que necesita:

| Entorno | Archivo | Cuándo se usa |
|---|---|---|
| Local | `config.settings.local` | Desarrollo. Incluye `debug_toolbar`. `DEBUG=True`. |
| Test | `config.settings.test` | Corriendo `pytest`. MD5 hasher, email en memoria. |
| UAT | `config.settings.uat` | Staging/QA. Hereda de `production`. |
| Producción | `config.settings.production` | Deploy real. HSTS, SSL redirect, Sentry, S3. |

Seleccionar un entorno específico:

```powershell
# PowerShell
$env:DJANGO_SETTINGS_MODULE = "config.settings.uat"
```

```bash
# bash / zsh
export DJANGO_SETTINGS_MODULE=config.settings.uat
```

Por defecto:

- `manage.py` apunta a `local`.
- `wsgi.py` / `asgi.py` apuntan a `production`.
- `pytest` usa `test` (configurado en `pyproject.toml`).

---

## Development workflow

### Dependencias

```bash
# Añadir una dependencia: editar requirements/<env>.in
# Luego recompilar el lockfile:
pip-compile requirements/local.in --output-file requirements/local.txt \
    --generate-hashes --allow-unsafe

#pip-compile requirements/base.in --output-file requirements/base.txt --generate-hashes --allow-unsafe
#pip-compile requirements/local.in --output-file requirements/local.txt --generate-hashes --allow-unsafe
#pip-compile requirements/uat.in --output-file requirements/uat.txt --generate-hashes --allow-unsafe
#pip-compile requirements/production.in --output-file requirements/production.txt --generate-hashes --allow-unsafe

# Sincronizar el venv exactamente con el lockfile
pip-sync requirements/local.txt
```

### Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### Correr el server

```bash
python manage.py runserver
```

### Shell interactivo con IPython

```bash
python manage.py shell
```

---

## Testing

```bash
# Todos los tests
pytest

# Tests de un app específico
pytest apps/users/

# Un test específico
pytest apps/users/tests/test_models.py::TestUserModel::test_pk_is_uuid

# Con coverage + report en HTML
pytest --cov --cov-report=term-missing --cov-report=html
# Abre htmlcov/index.html

# Recrear la BD de test (tras cambiar modelos)
pytest --create-db
```

La cobertura mínima del proyecto es **70%**. Si baja, `pytest --cov` falla con exit code ≠ 0.

---

## Code quality

### Ruff (lint + format)

```bash
# Auto-fix de issues + formateo
ruff check --fix .
ruff format .

# Solo verificación (sin cambios)
ruff check .
ruff format --check .
```

### Pre-commit

Se ejecuta automáticamente en cada `git commit`. Para correrlo manualmente sobre todo el repo:

```bash
pre-commit run --all-files
```

Actualizar las versiones de los hooks mensualmente:

```bash
pre-commit autoupdate
```

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'environ'`

Las dependencias no están instaladas. Ejecuta:

```bash
pip-sync requirements/local.txt
```

### `ImproperlyConfigured: Set the DJANGO_SECRET_KEY environment variable`

Falta el archivo `.env` o la variable `DJANGO_SECRET_KEY`. Generar una nueva con:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### `permission denied to create database` al correr tests

El usuario de Postgres no tiene permiso `CREATEDB`. Como superuser de Postgres:

```sql
ALTER USER dakshina CREATEDB;
```

### `database "test_bp_db" already exists`

Falló una corrida previa de tests. Fix:

```bash
pytest --create-db
```

### Ruff falla con `unknown variant 'py314'`

La versión del hook en `.pre-commit-config.yaml` quedó atrás. Actualizar:

```bash
pre-commit autoupdate
```

### Tests muy lentos (> 10s)

Verifica que `--reuse-db` esté activo en `pyproject.toml` y que estés usando `config.settings.test` (el hasher MD5 marca la diferencia). Revisa el encabezado que imprime `pytest`:

```text
django: version: 6.0, settings: config.settings.test (from ini)
```

---

## License

MIT (ajusta según el tipo de proyecto).
