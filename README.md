# 🌐 Microservicio de Traducción Inteligente (Smart Translator)

<div align="center">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Render](https://img.shields.io/badge/Render-%46E3B7.svg?style=for-the-badge&logo=render&logoColor=white)

<br>

[![Ver Demo en Vivo](https://img.shields.io/static/v1?label=Live&message=Ver%20Demo%20Swagger&color=success&style=for-the-badge)](https://smart-translator-api.onrender.com/docs)

<p>
  <b>Una API de traducción de alto rendimiento contenerizada, diseñada como un middleware inteligente sobre DeepL.</b><br>
  Optimizada para reducir costos y latencia, garantizando la seguridad mediante estrategias de <b>Rate Limiting</b> y <b>Caché</b>.
</p>

</div>

---

## 🏗 Arquitectura y Flujo

Este microservicio implementa el patrón **Cache-Aside** para minimizar las llamadas a APIs externas.

```mermaid
graph LR
    Client[Cliente] -->|HTTP/HTTPS| Gateway[Nginx / Render LB]
    Gateway -->|Proxy Pass| API[Servicio FastAPI]
    API -->|1. Verifica| Redis[(Caché Redis)]
    API -->|2. Fallback| DeepL[API DeepL]
    API -->|3. Registra| DB[(PostgreSQL)]
```

| Etapa            | Descripción                                                                                                                                                                                              |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ingreso**      | **Local:** Nginx actúa como Proxy Inverso en el puerto 80. **Cloud:** Render gestiona la capa SSL y el balanceo de carga.                                                                                |
| **Seguridad**    | El sistema aplica Rate Limiting (algoritmo Token Bucket) para prevenir abusos (defecto: 5 peticiones/min).                                                                                               |
| **Optimización** | **Hit:** Si la traducción existe en Redis, retorna inmediatamente (Latencia ~0ms, Costo $0). **Miss:** Si no existe, consulta a DeepL, guarda el resultado en caché (TTL 24h) y registra la transacción. |
| **Persistencia** | Todas las transacciones son auditadas en PostgreSQL para análisis histórico.                                                                                                                             |

---

## 🚀 Características Principales

- ⚡ **Caché Inteligente:** Utiliza Redis para almacenar traducciones recientes, reduciendo el consumo de la API externa hasta en un 90% para consultas repetitivas.

- 🛡️ **Gateway Robusto:** Configuración de Nginx personalizada como punto de entrada único, aislando la lógica de la aplicación del tráfico directo.

- 🚦 **Rate Limiting:** Protección contra ataques DDoS y control de cuotas mediante slowapi con almacenamiento en memoria.

- 📊 **Auditoría Persistente:** Registro asíncrono de cada petición en PostgreSQL utilizando SQLAlchemy.

- ☁️ **Cloud Native:** Arquitectura Dockerizada lista para desplegar en cualquier proveedor (Render, AWS, DigitalOcean).

---

## 🛠 Stack Tecnológico

| Componente    | Tecnología      | Rol                                              |
| ------------- | --------------- | ------------------------------------------------ |
| Lenguaje      | Python 3.13     | Lógica del núcleo                                |
| Framework     | FastAPI         | API REST Asíncrona                               |
| Gateway       | Nginx           | Proxy Inverso y Servidor Web                     |
| Base de Datos | PostgreSQL      | Datos Históricos y Auditoría                     |
| Caché         | Redis           | Almacenamiento rápido y Backend de Rate Limiting |
| CI/CD         | GitHub / Render | Despliegue continuo automático                   |
| Contenedor    | Docker Compose  | Orquestación de servicios                        |

---

## ⚙️ Configuración Local

### Prerrequisitos

- Docker y Docker Compose
- Una API Key de DeepL (Free o Pro)

### Instalación

**1. Clonar el repositorio:**

```bash
git clone https://github.com/TheMattGH/Smart-Translator-API.git
cd Smart-Translator-API
```

**2. Configurar Entorno:**

Crea un archivo `.env` en la raíz del proyecto.
(Docker priorizará la configuración interna para Redis/DB, solo necesitas tus claves externas):

```env
DEEPL_API_KEY=tu_clave_deepl_aqui
DEEPL_URL=https://api-free.deepl.com/v2/translate
```

**3. Construir y Levantar:**

```bash
docker-compose up --build
```

**4. Acceder:**

El servicio estará disponible a través de Nginx en el puerto 80:

- **Swagger UI:** http://localhost/docs

---

## 🔌 Ejemplo de Uso de la API (Producción)

Puedes probar la API directamente contra el servidor en la nube:

### Endpoint: `POST /translate`

```bash
curl -X 'POST' \
  'https://smart-translator-api.onrender.com/translate?text=Hello%20World&target_lang=ES' \
  -H 'accept: application/json' \
  -d ''
```

> **Nota:** El servicio está alojado en el plan gratuito de Render. Si no ha recibido tráfico recientemente, puede tardar hasta 50 segundos en "despertar" (Cold Start).

### Respuesta (Cache Miss - Obtenido de DeepL):

```json
{
  "original": "Hello World",
  "translated": "Hola Mundo",
  "source": "DEEPL API 🌍",
  "target_lang": "ES"
}
```

### Respuesta (Cache Hit - Latencia Cero):

```json
{
  "original": "Hello World",
  "translated": "Hola Mundo",
  "source": "CACHE (Redis) ⚡",
  "target_lang": "ES"
}
```

---

<div align="center">

Desarrollado con ❤️ por TheMattGH

</div>
