# SAFE - Seguridad Inteligente y Siempre Activa

Sistema de gestión de incidentes de seguridad ciudadana en Medellín, Colombia, utilizando GraphRAG con Zep para búsqueda semántica avanzada.

---

## Características Principales

| Módulo | Descripción |
|--------|-------------|
| **Autenticación** | Registro y login con nombre, email, contraseña y teléfono |
| **Dashboard** | Métricas visuales de incidentes por gravedad y ubicación |
| **GraphRAG** | Búsqueda semántica de incidentes usando Zep AI |
| **Incidentes** | Reporte geolocalizado con tipo, gravedad y barrio |
| **Alertas** | Centro de alertas críticas con notificaciones |

---

## Paleta de Colores SAFE

```
Primario:    #0A2463  (Azul oscuro corporativo)
Secundario:  #61A0AF  (Azul turquesa para highlights)
Fondo:       #F8F9FA  (Gris claro con degradado sutil)
Enfásis:     #FF6B6B  (Rojo coral para alertas críticas)
```

---

## Estructura del Proyecto

```
SAFE/
├── app.py              # Aplicación principal Streamlit
├── database.py         # Gestión SQLite (usuarios e incidentes)
├── graphrag.py         # Integración Zep GraphRAG
├── requirements.txt    # Dependencias Python
├── README.md           # Este archivo
└── .streamlit/
    ├── config.toml     # Configuración de tema y estilos
    └── secrets.toml    # Variables sensibles (API keys)
```

---

## Requisitos Previos

- Python 3.10+
- Cuenta en [Zep Cloud](https://www.zep.cloud) para GraphRAG
- Cuenta en [Streamlit Cloud](https://streamlit.io/cloud) para despliegue

---

## Instalación Local

```bash
# Clonar o navegar al directorio
cd SAFE

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app.py
```

---

## Configuración de Secrets

### Local (.streamlit/secrets.toml)
```toml
ZEP_API_KEY = "tu_api_key_de_zep_aqui"
```

### Streamlit Cloud
1. Ve a tu app en [share.streamlit.io](https://share.streamlit.io)
2. Abre **Settings** > **Secrets**
3. Agrega:
```toml
ZEP_API_KEY = "tu_api_key_de_zep_aqui"
```

---

## Despliegue en Streamlit Cloud

### Paso a Paso

1. **Preparar repositorio**
   ```bash
   git init
   git add .
   git commit -m "SAFE app - Initial commit"
   ```

2. **Subir a GitHub**
   - Crear repositorio en GitHub
   - Seguir instrucciones de push
   ```bash
   git remote add origin https://github.com/tu-usuario/safe-app.git
   git push -u origin main
   ```

3. **Configurar Streamlit Cloud**
   - Ir a [share.streamlit.io](https://share.streamlit.io)
   - Click en **New App**
   - Seleccionar repositorio y branch
   - Archivo principal: `app.py`
   - Agregar secrets en configuración avanzada

4. **Verificar despliegue**
   - Esperar ~2-3 minutos
   - Probar autenticación y registro

---

## API de Zep Cloud

La aplicación utiliza Zep para:

| Función | Descripción |
|---------|-------------|
| `add_incident_context()` | Indexa incidentes para búsqueda semántica |
| `search_incidents()` | Busca incidentes relacionados por similitud |
| `analyze_incident_patterns()` | Genera recomendaciones basadas en historial |

---

## Modelo de Datos

### Usuarios
```
id         (UUID)
nombre     (string)
email      (string, único)
password   (hash SHA256)
telefono   (string)
created_at (timestamp)
```

### Incidentes
```
id          (UUID)
user_id     (FK → users)
tipo        (string: hurto, robo vehicular, etc.)
descripcion (text)
ubicacion   (string)
barrio      (string)
gravedad    (enum: baja, media, alta, crítica)
estado      (enum: pendiente, procesando, resuelto)
fecha       (timestamp)
```

---

## Tipografía y UI

- **Títulos**: Montserrat Bold
- **Cuerpo**: Open Sans Regular
- **Botones**: Borde redondeado 12px, sombra suave
- **Navegación**: Bottom bar con 5 items (Inicio, Alertas, Incidentes, Perfil, Config)

---

## Seguridad

- Contraseñas hasheadas con SHA256
- Datos almacenados en SQLite local
- API keys en variables de entorno (no hardcodear)
- Contraste AA+ para accesibilidad

---

## Licencia

MIT License - Libre uso y modificación.

---

## Autor

SAFE - Seguridad Inteligente y Siempre Activa
Medellín, Colombia
