# SAFE - Seguridad Inteligente y Siempre Activa

Sistema fullstack de gestión de incidentes de seguridad en Medellín con **GraphRAG** (Zep) y **Agentes Predictivos IA**.

---

## Características

| Módulo | Descripción |
|--------|-------------|
| **Autenticación** | Registro/Login con nombre, email, contraseña, teléfono |
| **Dashboard** | Métricas, hotspots y visualización de grafos |
| **GraphRAG** | Búsqueda semántica con correlación geoespacial |
| **Incidentes** | Reporte con datos del usuario y ubicación |
| **Agentes Predictivos** | 4 agentes IA para predicción y análisis |
| **Perfil** | Historial y análisis personalizado |

---

## Sistema de Agentes Predictivos

| Agente | Función |
|--------|---------|
| 🌡️ **HotspotAgent** | Predice zonas calientes (barrios con más incidentes) |
| ⏰ **TemporalAgent** | Analiza patrones horarios y días pico |
| ⚠️ **RiskAgent** | Evalúa nivel de riesgo global |
| 🔗 **CorrelationAgent** | Encuentra correlaciones entre tipos de incidentes |

---

## GraphRAG con Zep

- **Grafos de correlación**: Nodos conectados por barrio/tipo
- **Hotspots**: Zonas con mayor frecuencia de incidentes
- **Búsqueda semántica**: Encuentra incidentes relacionados por similitud

---

## Paleta de Colores

```
Primario:    #0A2463
Secundario:  #61A0AF
Fondo:       #F8F9FA
Enfásis:     #FF6B6B
```

---

## Estructura

```
SAFE/
├── app.py               # Aplicación principal Streamlit
├── database.py          # Base de datos SQLite
├── graphrag.py          # Integración Zep GraphRAG
├── predictive_agents.py # Sistema de agentes IA
├── requirements.txt     # Dependencias
└── .streamlit/
    ├── config.toml      # Configuración de tema
    └── secrets.toml     # Secrets (ZEP_API_KEY)
```

---

## Instalación

```bash
cd SAFE
pip install -r requirements.txt
streamlit run app.py
```

---

## Secrets (Streamlit Cloud)

```toml
ZEP_API_KEY = "tu_api_key_de_zep"
```

---

## Flujo de Usuario

```
1. Registro (nombre, email, contraseña, teléfono)
2. Login
3. Dashboard con métricas
4. Reportar incidente (datos usuario + incidente)
5. Análisis predictivo con agentes
6. Búsqueda GraphRAG
```

---

## Modelo de Datos

**Usuarios**: id, nombre, email, password_hash, telefono, created_at

**Incidentes**: id, user_id, tipo, descripcion, ubicacion, barrio, gravedad, estado, fecha

---

Licencia: MIT
