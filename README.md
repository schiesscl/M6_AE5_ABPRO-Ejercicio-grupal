# Plataforma de Gestión de Eventos

## Hans Schiess
## Linwi Vargas

## Descripción del Proyecto

La **Plataforma de Gestión de Eventos** es una aplicación web desarrollada en Django que permite a los usuarios crear, gestionar y participar en eventos con un sistema de control de acceso basado en roles. El sistema implementa un modelo de permisos de tres niveles (Administradores, Organizadores y Asistentes) con capacidades específicas para cada rol.

## Características Principales

- **Gestión de Eventos CRUD**: Crear, leer, actualizar y eliminar eventos
- **Sistema de Roles**: Tres niveles de permisos (Administradores, Organizadores, Asistentes)
- **Registro de Usuarios**: Creación de cuentas nuevas con asignación automática de rol "Asistente"
- **Eventos Privados**: Control de visibilidad de eventos según permisos
- **Registro de Asistencia**: Los usuarios pueden registrarse a eventos
- **Interfaz Bootstrap 5**: Diseño moderno y responsivo
- **Autenticación**: Sistema de login/logout integrado con Django
- **Internacionalización**: Configurado en español (Chile)

## Requisitos del Sistema

### Tecnologías Principales

| Componente          | Tecnología      | Versión | Propósito                            |
| ------------------- | ---------------- | -------- | ------------------------------------- |
| Framework Web       | Django           | 5.2.8    | Framework principal de la aplicación |
| Lenguaje            | Python           | 3.12+    | Lenguaje de programación             |
| Base de Datos       | SQLite           | 3.x      | Base de datos de desarrollo           |
| Gestión de Config  | python-decouple  | 3.8      | Manejo de variables de entorno        |
| Motor de Plantillas | Django Templates | Built-in | Renderizado de HTML                   |
| ORM                 | Django ORM       | Built-in | Abstracción de base de datos         |
| Frontend            | Bootstrap        | 5.3.2    | Framework CSS                         |
| Iconos              | Bootstrap Icons  | 1.11.1   | Librería de iconos                   |

## Arquitectura del Sistema

La aplicación sigue el patrón **MVT (Model-View-Template)** de Django con clara separación de responsabilidades:

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐      ┌──────────────┐
│   Browser   │─────▶│  urls.py     │─────▶│  views.py   │─────▶│  models.py   │
│  (Cliente)  │      │  (Routing)   │      │  (Lógica)   │      │  (Datos)     │
└─────────────┘      └──────────────┘      └─────────────┘      └──────────────┘
       ▲                                           │                      │
       │                                           ▼                      ▼
       │                                    ┌─────────────┐      ┌──────────────┐
       └────────────────────────────────────│ templates/  │      │  db.sqlite3  │
                                            │  (HTML)     │      │  (Database)  │
                                            └─────────────┘      └──────────────┘
```

### Estructura de Directorios

```
M6_AE5_ABPRO-Ejercicio grupal/
├── event_platform/           # Configuración principal del proyecto Django
│   ├── __init__.py
│   ├── settings.py          # Configuración de la aplicación
│   ├── urls.py              # Enrutamiento principal
│   ├── wsgi.py              # Entrada WSGI para servidores
│   └── asgi.py              # Entrada ASGI para servidores
│
├── events/                   # Aplicación principal de eventos
│   ├── migrations/          # Migraciones de base de datos
│   ├── management/          # Comandos personalizados de Django
│   │   └── commands/
│   │       ├── setup_permissions.py    # Configuración de grupos y permisos
│   │       ├── create_test_users.py    # Creación de usuarios de prueba
│   │       └── check_permissions.py    # Verificación de permisos en BD
│   ├── templatetags/        # Filtros personalizados para templates
│   │   └── event_filters.py
│   ├── __init__.py
│   ├── admin.py             # Configuración del panel de administración
│   ├── apps.py              # Configuración de la aplicación
│   ├── models.py            # Modelos de datos (Event)
│   ├── permissions.py       # Lógica de permisos personalizados
│   ├── urls.py              # Rutas específicas de eventos
│   └── views.py             # Controladores de vistas
│
├── templates/               # Plantillas HTML
│   ├── base.html            # Plantilla base con navegación
│   ├── registration/
│   │   └── login.html       # Página de inicio de sesión
│   └── events/
│       ├── event_list.html          # Lista de eventos
│       ├── event_form.html          # Formulario de creación/edición
│       ├── event_confirm_delete.html # Confirmación de eliminación
│       └── access_denied.html       # Página de acceso denegado
│
├── db.sqlite3               # Base de datos SQLite
├── manage.py                # Script de gestión de Django
├── requirements.txt         # Dependencias del proyecto
├── .gitignore              # Archivos excluidos de Git
├── .env                    # Variables de entorno (NO subir a Git)
└── README.md               # Este archivo
```

## Modelo de Permisos y Roles

### Diagrama de Grupos y Permisos

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Django Auth System                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  User Model (django.contrib.auth.models.User)                       │
│                                                                      │
│                         belongs to                                  │
│                             │                                       │
│                             ▼                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Group Model                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│           │                    │                    │               │
│           ▼                    ▼                    ▼               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │
│  │ Administradores │  │  Organizadores  │  │   Asistentes    │   │
│  │  Full Access    │  │ Event Mgmt      │  │  View & Attend  │   │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘   │
│           │                    │                    │               │
│           │                    │                    │               │
│       Has all             Has all               Has all            │
│           │                    │                    │               │
│           ▼                    ▼                    ▼               │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                   Model Permissions                          │  │
│  ├─────────────────────────────────────────────────────────────┤  │
│  │ • add_event        • change_event     • delete_event        │  │
│  │ • view_event       • manage_event     • view_private_event  │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Tabla de Capacidades por Rol

| Grupo                     | Permisos de Modelo                                                | Permisos Personalizados                  | Capacidades                                                                        |
| ------------------------- | ----------------------------------------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------- |
| **Administradores** | `add_event`, `change_event`, `delete_event`, `view_event` | `manage_event`, `view_private_event` | Acceso completo: crear, editar, eliminar cualquier evento (público/privado)       |
| **Organizadores**   | `add_event`, `change_event`, `view_event`                   | `manage_event`, `view_private_event` | Crear eventos, editar propios eventos, ver todos los eventos                       |
| **Asistentes**      | `view_event`                                                    | Ninguno                                  | Ver eventos públicos, registrarse a eventos, ver eventos donde están registrados |

## Modelo de Datos

### Diagrama Entidad-Relación

```
┌─────────────────────────────────────────────┐
│                Event                        │
├─────────────────────────────────────────────┤
│ + CharField title                           │
│ + TextField description                     │
│ + CharField event_type                      │
│   - conference (Conferencia)                │
│   - concert (Concierto)                     │
│   - seminar (Seminario)                     │
│ + DateTimeField date                        │
│ + CharField location                        │
│ + BooleanField is_private                   │
│ + ForeignKey organizer ────────┐            │
│ + ManyToManyField attendees ───┼───┐        │
│ + DateTimeField created_at     │   │        │
│ + DateTimeField updated_at     │   │        │
└────────────────────────────────┼───┼────────┘
                                 │   │
                            1    │   │ many
                       organizer │   │ attendees
                                 │   │
                            1    │   │ many
                                 ▼   ▼
                        ┌─────────────────┐
                        │      User       │
                        ├─────────────────┤
                        │ + username      │
                        │ + email         │
                        │ + groups        │
                        └─────────────────┘
```

### Campos del Modelo Event

- **title**: Título del evento (máx. 200 caracteres)
- **description**: Descripción detallada del evento
- **event_type**: Tipo de evento (conference, concert, seminar)
- **date**: Fecha y hora del evento
- **location**: Ubicación del evento (máx. 255 caracteres)
- **is_private**: Indica si el evento es privado (solo visible para usuarios autorizados)
- **organizer**: Usuario que creó el evento (ForeignKey a User)
- **attendees**: Usuarios registrados al evento (ManyToManyField a User)
- **created_at**: Fecha de creación del registro
- **updated_at**: Fecha de última actualización

## Flujo de Solicitudes

### Ejemplo: Creación de un Evento

```
Browser ─────▶ GET /events/create/
                    │
                    ▼
        event_platform/urls.py ─────▶ include('events.urls')
                    │
                    ▼
               events/urls.py ─────▶ path('create/', ...)
                    │
                    ▼
          EventCreateView ─────▶ check_permission_required()
                    │                        │
                    │                [Has Permission]
                    │                        │
                    ▼                        ▼
      PermissionRequiredMixin ──────▶ Verify 'events.add_event'
                    │
                    ▼
         render(event_form.html)
                    │
                    ▼
              HTML form
                    │
         ┌──────────┴──────────┐
         │                     │
         ▼                     ▼
    [No Permission]      POST /events/create/
         │               {title, description, ...}
         │                     │
         ▼                     ▼
  handle_no_permission()  form_valid()
         │                     │
         │              "set organizer = request.user"
         │                     │
         ▼                     ▼
access_denied.html      Event.objects.create(...)
                                │
                                ▼
                         "INSERT INTO events_event"
                                │
                                ▼
                           db.sqlite3
                                │
                                ▼
                        "Success, return Event instance"
                                │
                                ▼
                         "Event object"
                                │
                                ▼
                      "Redirect to /events/"
                                │
                                ▼
Browser ◀────────────────── event_list.html
```

## Configuración e Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/event-platform.git
cd event-platform
```

### 2. Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Ejecutar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Configurar Grupos y Permisos

```bash
python manage.py setup_permissions
```

Este comando creará automáticamente los tres grupos (Administradores, Organizadores, Asistentes) con sus respectivos permisos.

### 7. Crear Usuarios de Prueba

```bash
python manage.py create_test_users
```

Este comando creará usuarios de ejemplo:

- **admin** / `admin123` (Administrador)
- **organizador** / `org123` (Organizador)
- **asistente** / `asist123` (Asistente)

También crea 3 eventos de ejemplo.

### `check_permissions`

Herramienta de auditoría para verificar la integridad de los permisos.

```bash
python manage.py check_permissions
```

### 8. Iniciar el Servidor

```bash
python manage.py runserver
```

La aplicación estará disponible en: **http://127.0.0.1:8000/**

## Autenticación y Acceso

### URLs de Autenticación

| URL          | Descripción                               |
| ------------ | ------------------------------------------ |
| `/signup/` | Página de registro de nuevos usuarios    |
| `/login/`  | Página de inicio de sesión               |
| `/logout/` | Cerrar sesión (POST)                      |
| `/admin/`  | Panel de administración de Django         |
| `/events/` | Lista de eventos (requiere autenticación) |

### Configuración de Redirecciones

```python
LOGIN_URL = '/login/'              # Redirige usuarios no autenticados
LOGIN_REDIRECT_URL = '/events/'    # Redirige después del login
LOGOUT_REDIRECT_URL = '/'          # Redirige después del logout
```

## Interfaz de Usuario

### Componentes de la UI

- **Navbar**: Navegación con menú desplegable de usuario
- **Cards de Eventos**: Muestra información del evento con badges de tipo y privacidad
- **Formularios**: Validación del lado del cliente y servidor
- **Mensajes Flash**: Notificaciones de éxito/error con Bootstrap alerts
- **Footer**: Pie de página fijo en la parte inferior

### Filtros de Template Personalizados

La aplicación incluye filtros personalizados para verificar permisos:

```django
{% load event_filters %}

{# Verificar si el usuario pertenece a un grupo #}
{% if user|has_group:"Administradores" %}
    <!-- Contenido solo para administradores -->
{% endif %}

{# Verificar si el usuario puede editar un evento #}
{% if user|can_edit_event:event %}
    <a href="{% url 'event_update' event.pk %}">Editar</a>
{% endif %}

{# Verificar si el usuario puede eliminar un evento #}
{% if user|can_delete_event:event %}
    <a href="{% url 'event_delete' event.pk %}">Eliminar</a>
{% endif %}
```

## Internacionalización

La aplicación está configurada para el idioma español (Chile):

```python
LANGUAGE_CODE = 'es'           # Idioma: Español
TIME_ZONE = 'America/Santiago' # Zona horaria: Santiago de Chile
USE_I18N = True                # Habilita internacionalización
USE_TZ = True                  # Habilita soporte de zonas horarias
```

## Comandos de Gestión Personalizados

### `setup_permissions`

Configura los grupos y permisos del sistema.

```bash
python manage.py setup_permissions
```

**Funcionalidad:**

- Crea los grupos: Administradores, Organizadores, Asistentes
- Asigna permisos de modelo a cada grupo
- Asigna permisos personalizados (manage_event, view_private_event)

### `create_test_users`

Crea usuarios de prueba con diferentes roles.

```bash
python manage.py create_test_users
```

**Usuarios creados:**

- `admin` (Administrador)
- `organizador` (Organizador)
- `asistente` (Asistente)

También crea 3 eventos de ejemplo.

### `check_permissions`

Herramienta de auditoría para verificar la integridad de los permisos.

```bash
python manage.py check_permissions
```

## Pruebas

### Ejecutar Tests

```bash
python manage.py test events
```

### Casos de Prueba Recomendados

- **Autenticación**: Login, logout, redirecciones
- **Permisos**: Verificar acceso por rol
- **CRUD de Eventos**: Crear, leer, actualizar, eliminar
- **Eventos Privados**: Visibilidad según permisos
- **Registro de Asistencia**: Agregar/quitar asistentes

## Despliegue

### Variables de Entorno para Producción

```env
SECRET_KEY=tu-secret-key-segura-aqui
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DATABASE_URL=postgres://user:pass@host:port/db
```

### Configuraciones Adicionales

```python
# settings.py para producción
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### Comandos de Producción

```bash
# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Aplicar migraciones
python manage.py migrate --noinput

# Crear superusuario
python manage.py createsuperuser
```

## Seguridad

### Mejores Prácticas Implementadas

- ✅ **CSRF Protection**: Tokens CSRF en todos los formularios
- ✅ **SQL Injection**: Uso de Django ORM
- ✅ **XSS Protection**: Escape automático de templates
- ✅ **Autenticación**: LoginRequiredMixin en vistas
- ✅ **Autorización**: PermissionRequiredMixin para permisos
- ✅ **Variables de Entorno**: Configuración sensible en `.env`

### Archivos Excluidos de Git

```gitignore
venv/
db.sqlite3
*.pyc
__pycache__/
.env
local_settings.py
```

## Contribución

### Flujo de Trabajo

1. Fork del repositorio
2. Crear rama de feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit de cambios: `git commit -m 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

### Estándares de Código

- Seguir [PEP 8](https://pep8.org/) para código Python
- Nombres de variables en inglés
- Comentarios y docstrings en español
- Máximo 79 caracteres por línea

---

**Fecha de creación:** Noviembre 2025

**Versión:** 1.0.0
