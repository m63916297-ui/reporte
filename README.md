# SAFE - Seguridad Inteligente y Siempre Activa

Aplicación fullstack para gestión de incidentes de seguridad en Medellín con GraphRAG.

## Características

- 🔐 **Autenticación**: Registro y login de usuarios
- 📊 **Dashboard**: Visualización de métricas e incidentes
- 🗣️ **GraphRAG**: Búsqueda semántica con Zep
- 📍 **Incidentes**: Reporte y consulta de incidentes por barrio
- 🎨 **Diseño**: Interfaz minimalista siguiendo los lineamientos SAFE

## Paleta de Colores

- **Primario**: `#0A2463` (Azul oscuro corporativo)
- **Secundario**: `#61A0AF` (Azul turquesa)
- **Fondo**: `#F8F9FA` (Gris claro)
- **Énfasis**: `#FF6B6B` (Rojo coral para alertas)

## Despliegue en Streamlit Cloud

1. Subir este código a un repositorio GitHub
2. Ir a [share.streamlit.io](https://share.streamlit.io)
3. Conectar el repositorio
4. Seleccionar `app.py` como archivo principal

## Variables de Entorno

En Streamlit Cloud, configurar en Secrets:

```toml
ZEP_API_KEY = "tu_api_key_de_zep"
```

## Estructura

```
SAFE/
├── app.py           # Aplicación principal Streamlit
├── database.py      # Base de datos SQLite
├── graphrag.py     # Integración Zep GraphRAG
├── requirements.txt # Dependencias
└── .streamlit/
    └── config.toml  # Configuración de tema
```

## Instalación local

```bash
pip install -r requirements.txt
streamlit run app.py
```
