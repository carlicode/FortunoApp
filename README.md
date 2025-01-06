## FortunoBot

FortunoBot es un bot de Telegram diseñado para administrar transacciones personales de ingresos y gastos, registrar categorías, y proporcionar un resumen del saldo actual de un usuario.

## Características

- Registrar ingresos y gastos: Agrega transacciones y clasifícalas por categorías.
- Consulta del saldo actual: Muestra el saldo disponible del usuario.
- Gestión de categorías: Lista las categorías disponibles o permite crear nuevas automáticamente al registrar transacciones.
- Comandos interactivos: Utiliza comandos de Telegram para una experiencia sencilla e intuitiva.

## Comandos disponibles

1. **/start**: Muestra un mensaje de bienvenida e instrucciones para usar el bot.
2. **/saldo**: Consulta el saldo actual del usuario.
3. **/ingreso [monto] [categoría]**: Registra un ingreso. Ejemplo: `/ingreso 500 Sueldo`.
4. **/gasto [monto] [categoría]**: Registra un gasto. Ejemplo: `/gasto 100 Comida`.
5. **/categorias**: Lista todas las categorías disponibles.

## Requisitos

- Python 3.9 o superior.
- Django 5.1.4.
- Una base de datos SQLite.
- Ngrok para establecer un túnel HTTPS.
- Un bot de Telegram configurado (obtener token desde BotFather).

## Instalación y configuración

Clona este repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd FortunoApp
```

Crea y activa un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Configura las variables de entorno:

Crea un archivo `.env` en la raíz del proyecto y agrega lo siguiente:

Aplica las migraciones:

```bash
python manage.py makemigrations finances
python manage.py migrate
```

Configura Ngrok:

Inicia un túnel HTTP con Ngrok:

```bash
ngrok http 8000
```

Copia la URL generada (por ejemplo: `https://37e7-189-28-80-120.ngrok-free.app`) y actualiza las variables en el archivo `.env` o directamente en `settings.py`:

```
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '37e7-189-28-80-120.ngrok-free.app']
```

Configura el webhook de Telegram:

```bash
curl -X POST "https://api.telegram.org/bot<TU_TOKEN>/setWebhook" \
     -d "url=https://<NGROK_URL>/webhook/"
```

### Uso

Inicia el servidor de Django:

```bash
python manage.py runserver
```

Envía comandos al bot desde Telegram y verifica su funcionamiento.

### Estructura del proyecto

```
FortunoApp/
├── finances/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── migrations/
│   └── templates/
├── fortuno/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── manage.py
└── requirements.txt
```

### Modelos

#### User

- **telegram_id**: ID único del usuario en Telegram.
- **username**: Nombre opcional del usuario.
- **created_at**: Fecha de registro.

#### UserBalance

- **user**: Relación uno a uno con el usuario.
- **balance**: Saldo actual del usuario.

#### Category

- **name**: Nombre único de la categoría.
- **description**: Descripción opcional.
- **created_at**: Fecha de creación.

#### Transaction

- **user**: Relación con el usuario.
- **category**: Relación con la categoría (opcional).
- **type**: Tipo de transacción (ingreso o gasto).
- **amount**: Monto de la transacción.
- **created_at**: Fecha de la transacción.

### Logs

Los logs son enviados a la consola para depuración. Se pueden configurar en `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
```

### Contribuciones

¡Las contribuciones son bienvenidas! Por favor, crea un fork del repositorio y envía un pull request con tus mejoras o sugerencias.

### Mejoras posibles

1. **Autenticación avanzada:**
   - Implementar autenticación basada en tokens para mayor seguridad.
   - Agregar soporte para múltiples usuarios con roles y permisos específicos.

2. **Mejoras en la interfaz del bot:**
   - Agregar botones interactivos en Telegram para facilitar la navegación.
   - Implementar menús dinámicos con opciones predefinidas para registrar transacciones.

3. **Soporte para múltiples idiomas:**
   - Añadir un sistema de internacionalización (i18n) para soportar diferentes idiomas.
   - Permitir a los usuarios seleccionar su idioma preferido.

4. **Integración con servicios externos:**
   - Conectar con APIs de bancos para sincronizar automáticamente transacciones.
   - Integrar con Google Sheets para exportar datos de ingresos y gastos.

5. **Análisis avanzado de datos:**
   - Generar gráficos y reportes detallados sobre las transacciones.
   - Implementar un sistema de alertas para notificar al usuario cuando se excedan presupuestos.

6. **Optimización de rendimiento:**
   - Implementar almacenamiento en caché para consultas frecuentes.
   - Migrar a una base de datos más robusta como PostgreSQL para escalar el proyecto.

7. **Soporte para OCR:**
   - Añadir funcionalidad para escanear facturas y recibos utilizando OCR.

8. **Despliegue en producción:**
   - Configurar despliegue automático en servicios como AWS, Heroku o DigitalOcean.
   - Implementar HTTPS utilizando un certificado SSL.

### Tecnologías recomendadas para producción

Para llevar este proyecto a producción, se recomienda utilizar las siguientes tecnologías:

- **Servidor de Aplicaciones:** Gunicorn o uWSGI para servir la aplicación Django.
- **Servidor Web:** Nginx para gestionar solicitudes HTTP y servir archivos estáticos.
- **Base de Datos:** PostgreSQL por su robustez y capacidad de escalabilidad.
- **Contenedores:** Docker para crear entornos consistentes y fáciles de desplegar.
- **Orquestador de Contenedores:** Kubernetes o Docker Swarm para gestionar el despliegue en múltiples nodos.
- **CI/CD:** GitHub Actions, GitLab CI/CD o Jenkins para automatizar pruebas y despliegues.
- **Monitoreo:** Prometheus y Grafana para supervisar el rendimiento y la disponibilidad del sistema.
- **Seguridad:** Let's Encrypt para certificados SSL gratuitos y mantener las conexiones seguras.
- **Backup:** Automatización de copias de seguridad de la base de datos con herramientas como pg_dump o servicios en la nube.

Implementando estas tecnologías, tu proyecto estará preparado para soportar un entorno de producción estable, escalable y seguro.
