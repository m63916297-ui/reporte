# 🛡️ SAFE - Seguridad Inteligente y Siempre Activa

Sistema fullstack de gestión de incidentes de seguridad ciudadana en Medellín, Colombia, utilizando **GraphRAG** (Zep), **Agentes Predictivos IA**, **análisis estadístico avanzado** y **geolocalización**.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Componentes](#-componentes)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Estructura](#-estructura)

---

## 🚀 Características

| Módulo | Descripción |
|--------|-------------|
| **Autenticación** | Registro/Login con validación SHA256 |
| **Dashboard** | Métricas, gráficos interactivos y alertas |
| **GraphRAG** | Búsqueda semántica y grafos de correlación |
| **Agentes IA** | 4 agentes predictivos para análisis |
| **Geolocalización** | Mapa de incidentes por ubicación |
| **Análisis Estadístico** | Visualizaciones avanzadas con NumPy + Plotly |
| **Emergencia 121** | Sistema SOS con contactos de emergencia |
| **Configuración AI** | Módulos de seguridad personalizables |

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Streamlit)                      │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────┤
│Dashboard │Incidentes│Predictivo│   SOS   │Contactos │ Settings │
├──────────┴──────────┴──────────┴──────────┴──────────┴──────────┤
│                     VISUALIZACIÓN (Plotly + NumPy)                │
├─────────────────────────────────────────────────────────────────┤
│                  AGENTES IA (Predictive Agents)                  │
│    HotspotAgent │ TemporalAgent │ RiskAgent │ CorrelationAgent   │
├─────────────────────────────────────────────────────────────────┤
│                    GRAPHRAG (Zep Cloud API)                      │
│         Incidente Graph │ Búsqueda Semántica │ Clusters         │
├─────────────────────────────────────────────────────────────────┤
│                    BASE DE DATOS (SQLite)                        │
│              Users │ Incidents │ Security Config                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Componentes

### 1. Dashboard Principal
```
┌─────────────────────────────────────────────────────────────────┐
│  🛡️ Dashboard SAFE - Medellín                                    │
├───────────────┬───────────────┬───────────────┬───────────────┬───┤
│    Total     │   Críticos    │     Altos    │  Mis Reportes │Riesgo│
│      42      │       5       │      12      │       8       │ 35% │
├───────────────┴───────────────┴───────────────┴───────────────┴───┤
│  [Analytics] [Geolocalización] [Grafo] [Tendencias]              │
│                                                                 │
│  ┌──────────────────────┐  ┌──────────────────────┐           │
│  │  Incidentes por      │  │  Distribución por      │           │
│  │  Barrio (Barras)     │  │  Tipo (Circular)      │           │
│  └──────────────────────┘  └──────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

**Funciones:**
- Métricas en tiempo real (total, críticos, altos, riesgo)
- Tabs de visualización: Analytics, Geolocalización, Grafo, Tendencias
- Gráficos interactivos con hover tooltips

---

### 2. Reporte de Incidentes
```
┌─────────────────────────────────────────────────────────────────┐
│  🚨 Reporte de Incidentes - Medellín                             │
├─────────────────────────────────────────────────────────────────┤
│  DATOS DEL REPORTANTE                                            │
│  ┌─────────────────┐  ┌─────────────────┐                     │
│  │ Nombre: Juan    │  │ Email: juan@... │                     │
│  └─────────────────┘  └─────────────────┘                     │
│  Teléfono: 300 123 4567                                       │
├─────────────────────────────────────────────────────────────────┤
│  DATOS DEL INCIDENTE                                            │
│  ┌─────────────────┐  ┌─────────────────┐                     │
│  │ Tipo: Hurto    ▼│  │ Gravedad: Alta ▼│                     │
│  └─────────────────┘  └─────────────────┘                     │
│                                                                 │
│  Descripción: ________________________________                 │
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐                     │
│  │ Dirección      │  │ Barrio: El      ▼│                     │
│  └─────────────────┘  └─────────────────┘                     │
│                                                                 │
│  📍 Geolocalización                                            │
│  ┌─────────────────┐  ┌─────────────────┐                     │
│  │ Lat: 6.208763  │  │ Lon: -75.5685   │                     │
│  └─────────────────┘  └─────────────────┘                     │
│                                                                 │
│  ┌─────────────────────────────────────────┐                   │
│  │         💾 REPORTAR INCIDENTE          │                   │
│  └─────────────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

**Campos:**
- Datos del reportante (pre-cargados desde registro)
- Tipo de incidente (Hurto, Robo vehicular, Vandalismo, etc.)
- Nivel de gravedad (Baja, Media, Alta, Crítica)
- Descripción detallada
- Ubicación y barrio
- Geolocalización opcional (lat/lon)

---

### 3. Análisis Predictivo con Agentes IA

#### Agente HotspotAgent (🌡️)
```
Predice zonas calientes donde es más probable que ocurran incidentes
basándose en frecuencia histórica y patrones geográficos.
```
- Identifica barrios con mayor concentración de incidentes
- Calcula nivel de riesgo por zona
- Predice cantidad de incidentes probables

#### Agente TemporalAgent (⏰)
```
Analiza patrones temporales para identificar horarios y días
con mayor probabilidad de incidentes.
```
- Distribución por hora del día
- Distribución por día de la semana
- Identificación de horarios pico

#### Agente RiskAgent (⚠️)
```
Evalúa el nivel de riesgo general basándose en la gravedad
de los incidentes reportados.
```
- Score de riesgo ponderado (0-100)
- Clasificación: Bajo, Medio, Alto, Crítico
- Recomendaciones de seguridad

#### Agente CorrelationAgent (🔗)
```
Encuentra correlaciones entre tipos de incidentes y ubicaciones
para identificar patrones complejos.
```
- Tipos de incidentes correlacionados por barrio
- Fuerza de correlación
- Insights de relaciones

**Visualización:**
```
┌─────────────────────────────────────────────────────────────────┐
│  🔮 Análisis Predictivo con Agentes IA                           │
├─────────────────────────────────────────────────────────────────┤
│  Nivel de Riesgo: ⚠️ ALTO    Confianza: 87%    Agentes: 4     │
├─────────────────────────────────────────────────────────────────┤
│  [Hotspots] [Temporal] [Riesgo] [Correlación]                 │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │         Hotspots Predichos (Scatter Plot)               │   │
│  │                                                      │   │
│  │    ● El Poblado      ● Laureles      ● Centro        │   │
│  │    ● Robledo        ● Buenos Aires  ● Manrique      │   │
│  │                                                      │   │
│  │    Tamaño = Incidentes históricos                   │   │
│  │    Color = Nivel de riesgo                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Recomendaciones:                                              │
│  - 📍 El Poblado: 12 incidentes predichos (ALTO)             │
│  - 📍 Laureles: 8 incidentes predichos (MEDIO)              │
└─────────────────────────────────────────────────────────────────┘
```

---

### 4. GraphRAG con Zep Cloud

```
┌─────────────────────────────────────────────────────────────────┐
│  🔗 Grafo de Correlación (GraphRAG)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│       [N1]───────────────[N2]                                   │
│        │                │                                       │
│        │    ┌───────────┘                                       │
│        │    │                                                   │
│        ▼    ▼                                                   │
│      [N3]──[N4]────────[N5]                                   │
│        │                │                                       │
│        └───────┬────────┘                                      │
│                │                                               │
│                ▼                                               │
│              [N6]                                               │
│                                                                 │
│  N1-N6 = Nodos (Incidentes)                                   │
│  Líneas = Conexiones (Mismo barrio/tipo)                      │
│  Colores = Barrios                                            │
│                                                                 │
│  Leyenda: 🔵 El Poblado  🔵 Laureles  🔵 Centro             │
│                                                                 │
│  Nodos: 6  │  Conexiones: 8                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Funcionalidades:**
- `add_incident_context()` - Agrega incidente al índice semántico
- `create_incident_graph()` - Crea nodo en colección graph
- `build_incident_graph()` - Construye grafo de correlación
- `search_incidents()` - Búsqueda semántica por similitud
- `get_hotspots()` - Identifica zonas calientes

---

### 5. Geolocalización

```
┌─────────────────────────────────────────────────────────────────┐
│  📍 Mapa de Incidentes por Ubicación                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    🗺️ OpenStreetMap                    │   │
│  │                                                      │   │
│  │         ● El Poblado (12)                           │   │
│  │              ● Laureles (8)                         │   │
│  │                   ● Centro (15)                       │   │
│  │                        ● Robledo (6)                 │   │
│  │                         ● Belén (4)                    │   │
│  │                                                      │   │
│  │    Tamaño del marcador = Cantidad de incidentes     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Coords: 6.2447, -75.5700 (Medellín, Colombia)               │
└─────────────────────────────────────────────────────────────────┘
```

**Datos de prueba por barrio:**
| Barrio | Latitud | Longitud |
|--------|---------|----------|
| El Poblado | 6.2087 | -75.5685 |
| Laureles | 6.2445 | -75.5900 |
| Belén | 6.2297 | -75.6032 |
| Centro | 6.2442 | -75.5750 |
| Robledo | 6.2667 | -75.5667 |

---

### 6. Análisis Estadístico Avanzado

```
┌─────────────────────────────────────────────────────────────────┐
│  📊 Analytics - Análisis Estadístico Avanzado                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐  ┌──────────────────────┐           │
│  │ Distribución por     │  │ Tendencias           │           │
│  │ Gravedad             │  │ Temporales           │           │
│  │ ████████████ Alta    │  │ 📈 ───────          │           │
│  │ ████████ Crítica     │  │     ╱               │           │
│  │ ████ Media           │  │ ─────╱ ─────        │           │
│  │ ██ Baja              │  │                      │           │
│  └──────────────────────┘  └──────────────────────┘           │
│                                                                 │
│  ┌──────────────────────┐  ┌──────────────────────┐           │
│  │ Mapa de Calor       │  │ Top 10 Barrios      │           │
│  │ Tipo x Barrio       │  │                     │           │
│  │  Hurto  Robo  Vand  │  │ ██████████████ El P  │           │
│  │ El Pob  ██   ██   ██│  │ ███████████ Laure  │           │
│  │ Laure  ██   ██   ██│  │ ████████ Centro    │           │
│  │ Centro ██   ██   ██│  │ ██████ Robledo     │           │
│  └──────────────────────┘  └──────────────────────┘           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Gráficos generados con NumPy + Plotly:**
- Barras horizontales (barrios)
- Circular/torta (tipos, gravedad)
- Línea temporal (tendencias)
- Heatmap (tipo × barrio)
- Scatter (hotspots predichos)
- Gauge/Indicador (nivel de riesgo)
- Red/Grafo (correlaciones)

---

### 7. Sistema de Emergencia 121

```
┌─────────────────────────────────────────────────────────────────┐
│  🚨 EMERGENCIA 121                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │  🚨 POLICÍA │  │ 🚑AMBULANCIA│  │  🚒 BOMBEROS│           │
│  │             │  │             │  │             │           │
│  │     123     │  │     123     │  │     119     │           │
│  │             │  │             │  │             │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                                 │
│  CONTACTOS PERSONALES                                          │
│  📱 María López: 300 123 4567 (Familiar)                      │
│  📱 Juan García: 310 987 6543 (Amigo)                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Contactos de emergencia Medellín:**
- 🚨 Policía Nacional: 123
- 🚑 Ambulancia/ECCO: 123
- 🚒 Bomberos: 119

---

### 8. Configuración AI de Seguridad

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚙️ Configuración de Seguridad AI                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  MÓDULOS DE PROTECCIÓN                                        │
│  ┌─────────────────────────┐  ┌─────────────────────────┐    │
│  │ 🛡️ Privacidad           │  │ 🔐 AI Predictivo        │    │
│  │ [✓] Anonimizar datos   │  │ [✓] Análisis IA       │    │
│  │ [✓] Geolocalización     │  │ [✓] Alertas predict.  │    │
│  │ [✓] Notificaciones      │  │ [✓] Cifrado datos     │    │
│  └─────────────────────────┘  └─────────────────────────┘    │
│                                                                 │
│  POLÍTICAS DE SEGURIDAD                                       │
│  ✅ Datos cifrados en tránsito (TLS)                           │
│  ✅ Contraseñas hasheadas SHA256                                │
│  ✅ Cumplimiento Ley Habeas Data (Colombia)                    │
│  ✅ Sesiones con timeout automático                            │
│  ✅ Registro de actividad                                       │
│  ✅ AI de detección de anomalías                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Opciones configurables:**
| Opción | Descripción |
|--------|-------------|
| Anonimizar datos | No vincula datos personales a incidentes |
| Geolocalización | Permite registrar coordenadas exactas |
| Análisis IA | Activa predicción de incidentes |
| Alertas predictivas | Notificaciones proactivas |
| Cifrado de datos | Cifra datos sensibles |
| Notificaciones | Alertas push de seguridad |

---

## 🛠️ Tecnologías

| Tecnología | Uso |
|------------|-----|
| **Python 3.10+** | Lenguaje principal |
| **Streamlit** | Framework de visualización |
| **Pandas** | Manipulación de datos |
| **NumPy** | Cálculos numéricos |
| **Plotly** | Visualizaciones interactivas |
| **SQLite** | Base de datos local |
| **Zep Cloud** | GraphRAG y búsqueda semántica |
| **SHA256** | Hash de contraseñas |

---

## 📥 Instalación

```bash
# Clonar o navegar al directorio
cd SAFE

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app.py
```

### requirements.txt
```
streamlit>=1.28.0
zep-cloud>=1.0.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
```

---

## ⚙️ Configuración

### Variables de Entorno

```bash
# Linux/Mac
export ZEP_API_KEY="tu_api_key_de_zep"

# Windows (CMD)
set ZEP_API_KEY=tu_api_key_de_zep

# Windows (PowerShell)
$env:ZEP_API_KEY="tu_api_key_de_zep"
```

### Streamlit Cloud Secrets

En el dashboard de Streamlit Cloud, agregar en **Settings > Secrets**:

```toml
ZEP_API_KEY = "tu_api_key_de_zep"
```

### Obtener API Key de Zep

1. Ir a [Zep Cloud](https://www.zep.cloud)
2. Crear cuenta
3. Ir a Dashboard > API Keys
4. Copiar la clave

---

## 📁 Estructura

```
SAFE/
├── app.py                    # Aplicación principal (Streamlit)
├── database.py               # Gestión de base de datos (SQLite)
├── graphrag.py               # Integración Zep GraphRAG
├── predictive_agents.py      # Sistema de 4 agentes IA
├── requirements.txt         # Dependencias Python
├── README.md                 # Este archivo
└── .streamlit/
    ├── config.toml           # Configuración de tema
    └── secrets.toml          # Secrets (ZEP_API_KEY)
```

---

## 🔐 Seguridad

- Contraseñas hasheadas con SHA256
- Datos almacenados localmente en SQLite
- API keys en variables de entorno (nunca hardcodear)
- Sesiones con expiración
- Cumplimiento Ley de Habeas Data (Colombia)

---

## 📊 Modelo de Datos

### Usuarios
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | TEXT (UUID) | Identificador único |
| nombre | TEXT | Nombre completo |
| email | TEXT UNIQUE | Correo electrónico |
| password_hash | TEXT | Hash SHA256 |
| telefono | TEXT | Número de teléfono |
| created_at | TIMESTAMP | Fecha de registro |

### Incidentes
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | TEXT (UUID) | Identificador único |
| user_id | TEXT (FK) | Referencia a usuario |
| tipo | TEXT | Categoría del incidente |
| descripcion | TEXT | Descripción detallada |
| ubicacion | TEXT | Dirección exacta |
| barrio | TEXT | Barrio de Medellín |
| gravedad | TEXT | baja/media/alta/crítica |
| estado | TEXT | pendiente/procesando/resuelto |
| fecha | TIMESTAMP | Fecha y hora |
| lat | REAL | Latitud (opcional) |
| lon | REAL | Longitud (opcional) |

---

## 🌐 Barrios de Medellín Soportados

- El Poblado
- Laureles
- Belén
- Centro
- Robledo
- Villa Hermosa
- Buenos Aires
- Manrique
- Aranjuez
- Castilla
- Otro

---

## 📈 Flujo de Usuario

```
1. Registro (nombre, email, contraseña, teléfono)
          ↓
2. Login con credenciales
          ↓
3. Dashboard con métricas generales
          ↓
     ┌───┴───┬────────┬────────┬──────┐
     ↓       ↓        ↓        ↓      ↓
  Reporte  Analytics  SOS    Predictivo  Settings
  Incidente (Gráficos) 121  Agentes IA
     ↓       ↓        ↓        ↓      ↓
  GraphRAG Stats    Contactos Config AI
  (Zep)    Plotly  Emergencia
          ↓
4. Análisis predictivo con agentes IA
          ↓
5. Visualización de grafos y correlaciones
```

---

## 🎯 Casos de Uso

1. **Ciudadano reporta incidente** → Se guarda en BD y se indexa en GraphRAG
2. **Sistema identifica hotspots** → Agente predice zonas de riesgo
3. **Usuario consulta grafo** → GraphRAG muestra correlaciones
4. **Emergencia 121** → Acceso rápido a servicios de secours
5. **Análisis de tendencias** → Plotly visualiza patrones temporales

---

## 📝 Licencia

MIT License - Libre uso y modificación.

---

## 👨‍💻 Autor

**SAFE - Seguridad Inteligente y Siempre Activa**  
Medellín, Colombia  
GraphRAG powered by [Zep Cloud](https://www.zep.cloud)

---

<div align="center">

**🛡️ Protegiendo a Medellín con Inteligencia Artificial**

</div>
