import streamlit as st
import database as db
import graphrag as grag
from datetime import datetime

st.set_page_config(
    page_title="SAFE - Seguridad Inteligente",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

SAFE_COLORS = {
    "primary": "#0A2463",
    "secondary": "#61A0AF",
    "background": "#F8F9FA",
    "emphasis": "#FF6B6B",
    "text": "#0A2463",
    "white": "#FFFFFF",
}

FONT_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Open+Sans:wght@400;600&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #F8F9FA 0%, #E8ECEF 100%);
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        color: #0A2463 !important;
    }
    
    body, p, span, div {
        font-family: 'Open Sans', sans-serif !important;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .logo-title {
        font-size: 3rem !important;
        font-weight: 700 !important;
        color: #0A2463 !important;
        letter-spacing: 4px;
    }
    
    .logo-subtitle {
        font-size: 1rem;
        color: #61A0AF;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    .auth-card {
        background: white;
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(10, 36, 99, 0.12);
        max-width: 420px;
        margin: 0 auto;
    }
    
    .stButton > button {
        background-color: #0A2463 !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 12px rgba(10, 36, 99, 0.2) !important;
        transition: all 0.3s ease !important;
        min-height: 48px !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background-color: #0d2d52 !important;
        transform: scale(0.98);
        box-shadow: 0 2px 8px rgba(10, 36, 99, 0.3) !important;
    }
    
    .stButton > button:active {
        transform: scale(0.95);
    }
    
    .secondary-btn > button {
        background-color: transparent !important;
        color: #0A2463 !important;
        border: 2px solid #61A0AF !important;
    }
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 12px !important;
        border: 1px solid #E0E0E0 !important;
        padding: 0.75rem !important;
        font-family: 'Open Sans', sans-serif !important;
        background-color: #FAFAFA !important;
        min-height: 48px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #61A0AF !important;
        box-shadow: 0 0 0 2px rgba(97, 160, 175, 0.2) !important;
    }
    
    .stSelectbox > div > div {
        border-radius: 12px !important;
        min-height: 48px !important;
    }
    
    .nav-bar {
        display: flex;
        justify-content: space-around;
        background: white;
        padding: 1rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(10, 36, 99, 0.1);
        margin-bottom: 2rem;
        position: sticky;
        bottom: 0;
    }
    
    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        color: #0A2463;
        cursor: pointer;
        padding: 0.5rem 1rem;
        border-radius: 12px;
        transition: all 0.3s ease;
        min-width: 60px;
    }
    
    .nav-item:hover {
        background: rgba(10, 36, 99, 0.05);
    }
    
    .nav-item.active {
        background: rgba(10, 36, 99, 0.1);
    }
    
    .nav-icon {
        font-size: 1.5rem;
        margin-bottom: 0.25rem;
    }
    
    .nav-label {
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(10, 36, 99, 0.08);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(10, 36, 99, 0.12);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0A2463;
        font-family: 'Montserrat', sans-serif !important;
    }
    
    .metric-label {
        color: #61A0AF;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    .alert-badge {
        background: #FF6B6B;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .incident-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(10, 36, 99, 0.08);
        margin-bottom: 1rem;
        border-left: 4px solid #61A0AF;
    }
    
    .incident-card.critica { border-left-color: #FF6B6B; }
    .incident-card.alta { border-left-color: #FF8C00; }
    .incident-card.media { border-left-color: #FFD700; }
    .incident-card.baja { border-left-color: #4CAF50; }
    
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .status-badge.pendiente { background: #FFF3CD; color: #856404; }
    .status-badge.procesando { background: #D1ECF1; color: #0C5460; }
    .status-badge.resuelto { background: #D4EDDA; color: #155724; }
    
    .logout-btn > button {
        background-color: transparent !important;
        color: #FF6B6B !important;
        border: 2px solid #FF6B6B !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 1rem 2rem !important;
        color: #61A0AF !important;
        font-weight: 600 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #0A2463 !important;
        color: white !important;
    }
    
    .user-info {
        background: linear-gradient(135deg, #0A2463 0%, #1a3a7a 100%);
        padding: 1.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .user-avatar {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: #61A0AF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    div[data-testid="stForm"] {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(10, 36, 99, 0.12);
    }
    
    .success-box {
        background: #D4EDDA;
        border: 1px solid #C3E6CB;
        border-radius: 12px;
        padding: 1rem;
        color: #155724;
    }
    
    .error-box {
        background: #F8D7DA;
        border: 1px solid #F5C6CB;
        border-radius: 12px;
        padding: 1rem;
        color: #721C24;
    }
</style>
"""


def apply_custom_styles():
    st.markdown(FONT_CSS, unsafe_allow_html=True)


def show_logo():
    st.markdown(
        """
        <div class="main-header">
            <h1 class="logo-title">🛡️ SAFE</h1>
            <p class="logo-subtitle">Seguridad Inteligente y Siempre Activa</p>
        </div>
    """,
        unsafe_allow_html=True,
    )


def show_bottom_nav(current_page: str, is_logged_in: bool):
    nav_items = [
        ("🏠", "Inicio", "home"),
        ("🔔", "Alertas", "alerts"),
        ("📊", "Incidentes", "incidents"),
        ("👤", "Perfil", "profile"),
        ("⚙️", "Config", "settings"),
    ]

    cols = st.columns(5)
    for i, (icon, label, page) in enumerate(nav_items):
        with cols[i]:
            if page == current_page:
                st.markdown(
                    f"""
                    <div class="nav-item active">
                        <span class="nav-icon">{icon}</span>
                        <span class="nav-label">{label}</span>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="nav-item">
                        <span class="nav-icon">{icon}</span>
                        <span class="nav-label">{label}</span>
                    </div>
                """,
                    unsafe_allow_html=True,
                )


def init_session_state():
    if "user" not in st.session_state:
        st.session_state.user = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"
    if "graphrag" not in st.session_state:
        st.session_state.graphrag = grag.create_graphrag_service()


def render_register_form():
    apply_custom_styles()
    show_logo()

    st.markdown('<div class="auth-card">', unsafe_allow_html=True)

    st.markdown("### 📝 Registro de Usuario")
    st.markdown("*Crea tu cuenta para acceder a SAFE*")

    with st.form("register_form", clear_on_submit=True):
        nombre = st.text_input("Nombre completo", placeholder="Ej: Juan Pérez")
        email = st.text_input(
            "Email", placeholder="Ej: juan@ejemplo.com", type="default"
        )
        password = st.text_input(
            "Contraseña", placeholder="Mínimo 6 caracteres", type="password"
        )
        telefono = st.text_input("Teléfono", placeholder="Ej: 300 123 4567", type="tel")

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Registrarse")
        with col2:
            if st.form_submit_button(
                "Ya tengo cuenta", kwargs={"form_id": "login_nav"}
            ):
                st.session_state.current_page = "login"
                st.rerun()

        if submitted:
            if not all([nombre, email, password, telefono]):
                st.markdown(
                    '<div class="error-box">Por favor completa todos los campos</div>',
                    unsafe_allow_html=True,
                )
            else:
                success, msg = db.create_user(nombre, email, password, telefono)
                if success:
                    st.markdown(
                        f'<div class="success-box">✅ {msg}</div>',
                        unsafe_allow_html=True,
                    )
                    st.session_state.current_page = "login"
                    st.rerun()
                else:
                    st.markdown(
                        f'<div class="error-box">❌ {msg}</div>', unsafe_allow_html=True
                    )

    st.markdown("</div>", unsafe_allow_html=True)


def render_login_form():
    apply_custom_styles()
    show_logo()

    st.markdown('<div class="auth-card">', unsafe_allow_html=True)

    st.markdown("### 🔐 Iniciar Sesión")
    st.markdown("*Accede a tu cuenta SAFE*")

    with st.form("login_form", clear_on_submit=True):
        email = st.text_input("Email", placeholder="tu@email.com", type="default")
        password = st.text_input(
            "Contraseña", placeholder="Tu contraseña", type="password"
        )

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Ingresar")
        with col2:
            if st.form_submit_button(
                "Crear cuenta", kwargs={"form_id": "register_nav"}
            ):
                st.session_state.current_page = "register"
                st.rerun()

        if submitted:
            user = db.verify_user(email, password)
            if user:
                st.session_state.user = user
                st.session_state.current_page = "home"
                st.rerun()
            else:
                st.markdown(
                    '<div class="error-box">❌ Email o contraseña incorrectos</div>',
                    unsafe_allow_html=True,
                )

    st.markdown("</div>", unsafe_allow_html=True)


def render_home():
    apply_custom_styles()

    if not st.session_state.user:
        st.session_state.current_page = "login"
        st.rerun()
        return

    user = st.session_state.user

    st.markdown(
        f"""
        <div class="user-info">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div class="user-avatar">{user["nombre"][0].upper()}</div>
                <div>
                    <h3 style="margin: 0; color: white;">Bienvenido, {user["nombre"]}</h3>
                    <p style="margin: 0; opacity: 0.8;">{user["email"]}</p>
                </div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    stats = db.get_incident_stats()

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{stats.get("total", 0)}</div>
                <div class="metric-label">Total Incidentes</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        criticos = stats.get("por_gravedad", {}).get("crítica", 0)
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #FF6B6B;">{criticos}</div>
                <div class="metric-label">Casos Críticos</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #61A0AF;">🛡️</div>
                <div class="metric-label">SAFE Activo</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("### 🚨 Últimas Alertas en Medellín")

    if st.session_state.graphrag.is_available():
        patterns = st.session_state.graphrag.analyze_incident_patterns(user["id"])
        if patterns.get("recommendations"):
            st.markdown("#### 📊 Análisis Personalizado")
            for rec in patterns["recommendations"]:
                st.info(rec)

    incidents = db.get_incidents(user["id"])[:5]

    if incidents:
        for inc in incidents:
            gravedad_class = inc.get("gravedad", "baja").lower()
            st.markdown(
                f"""
                <div class="incident-card {gravedad_class}">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <strong style="color: #0A2463;">{inc.get("tipo", "N/A")}</strong>
                            <p style="margin: 0.5rem 0; color: #555;">{inc.get("descripcion", "N/A")}</p>
                            <small style="color: #888;">📍 {inc.get("barrio", "N/A")} • {inc.get("ubicacion", "N/A")}</small>
                        </div>
                        <span class="status-badge {inc.get("estado", "pendiente")}">{inc.get("estado", "pendiente")}</span>
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No tienes incidentes reportados. ¡Mantente seguro! 🛡️")

    if st.button("🚨 Reportar Nuevo Incidente", type="primary"):
        st.session_state.current_page = "incidents"
        st.rerun()


def render_alerts():
    apply_custom_styles()

    st.markdown("### 🔔 Centro de Alertas")

    stats = db.get_incident_stats()
    alertas = stats.get("por_gravedad", {}).get("crítica", 0) + stats.get(
        "por_gravedad", {}
    ).get("alta", 0)

    if alertas > 0:
        st.markdown(
            f"""
            <div class="alert-badge">
                🔔 {alertas} alertas activas requieren atención
            </div>
        """,
            unsafe_allow_html=True,
        )

    tab1, tab2 = st.tabs(["📍 Por Ubicación", "📊 Por Tipo"])

    with tab1:
        top_barrios = stats.get("top_barrios", {})
        if top_barrios:
            for barrio, count in list(top_barrios.items())[:5]:
                st.markdown(
                    f"""
                    <div class="incident-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong style="color: #0A2463;">📍 {barrio}</strong>
                            <span style="background: #FF6B6B; color: white; padding: 0.25rem 0.75rem; border-radius: 20px;">{count}</span>
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No hay alertas por ubicación")

    with tab2:
        por_tipo = stats.get("por_tipo", {})
        if por_tipo:
            for tipo, count in por_tipo.items():
                st.markdown(
                    f"""
                    <div class="incident-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong style="color: #0A2463;">{tipo}</strong>
                            <span style="background: #61A0AF; color: white; padding: 0.25rem 0.75rem; border-radius: 20px;">{count}</span>
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No hay alertas por tipo")


def render_incidents():
    apply_custom_styles()

    st.markdown("### 📊 Gestión de Incidentes")
    st.markdown("*Reporta y consulta incidentes de seguridad en Medellín*")

    tab1, tab2, tab3 = st.tabs(["➕ Reportar", "📋 Mis Reportes", "🔍 Consultar"])

    with tab1:
        st.markdown("#### Nuevo Reporte de Incidente")

        with st.form("incident_form", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                tipo = st.selectbox(
                    "Tipo de incidente",
                    [
                        "Seleccionar...",
                        "Hurto",
                        "Robo vehicular",
                        "Vandalismo",
                        "Agresión",
                        "Accidente de tránsito",
                        "Incendio",
                        "Daño a infraestructura",
                        "Otro",
                    ],
                )

            with col2:
                gravedad = st.selectbox(
                    "Nivel de gravedad", ["baja", "media", "alta", "crítica"]
                )

            descripcion = st.text_area(
                "Descripción detallada", placeholder="Describe el incidente..."
            )

            col3, col4 = st.columns(2)

            with col3:
                ubicacion = st.text_input(
                    "Dirección", placeholder="Ej: Cra. 48 #Sur-45"
                )

            with col4:
                barrio = st.text_input("Barrio", placeholder="Ej: El Poblado")

            submitted = st.form_submit_button("💾 Reportar Incidente", type="primary")

            if submitted and tipo != "Seleccionar...":
                user_id = st.session_state.user["id"]
                incident_id = db.save_incident(
                    user_id, tipo, descripcion, ubicacion, barrio, gravedad
                )

                incident_data = {
                    "id": incident_id,
                    "tipo": tipo,
                    "descripcion": descripcion,
                    "ubicacion": ubicacion,
                    "barrio": barrio,
                    "gravedad": gravedad,
                    "user_id": user_id,
                }

                st.session_state.graphrag.add_incident_context(user_id, incident_data)

                st.markdown(
                    '<div class="success-box">✅ Incidente reportado exitosamente</div>',
                    unsafe_allow_html=True,
                )

    with tab2:
        user_incidents = db.get_incidents(st.session_state.user["id"])

        if user_incidents:
            for inc in user_incidents:
                gravedad_class = inc.get("gravedad", "baja").lower()
                st.markdown(
                    f"""
                    <div class="incident-card {gravedad_class}">
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <strong style="color: #0A2463;">{inc.get("tipo")}</strong>
                                <p style="margin: 0.25rem 0;">{inc.get("descripcion", "Sin descripción")}</p>
                                <small style="color: #888;">
                                    📍 {inc.get("barrio", "N/A")} | 
                                    🕐 {inc.get("fecha", "N/A")}
                                </small>
                            </div>
                            <span class="status-badge {inc.get("estado", "pendiente")}">{inc.get("estado")}</span>
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No has reportado incidentes")

    with tab3:
        st.markdown("#### Búsqueda con GraphRAG")
        query = st.text_input(
            "Buscar incidentes relacionados", placeholder="Ej: hurtos en El Poblado..."
        )

        if query and st.button("🔍 Buscar"):
            if st.session_state.graphrag.is_available():
                results = st.session_state.graphrag.search_incidents(query)
                if results:
                    st.markdown(f"**{len(results)} resultados encontrados:**")
                    for r in results:
                        st.markdown(
                            f"""
                            <div class="incident-card">
                                <p>{r.get("content", "")}</p>
                                <small>Similitud: {r.get("score", 0):.2f}</small>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.info("No se encontraron resultados")
            else:
                st.warning(
                    "GraphRAG no está disponible. Asegúrate de configurar ZEP_API_KEY."
                )


def render_profile():
    apply_custom_styles()

    user = st.session_state.user

    st.markdown("### 👤 Mi Perfil")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(
            f"""
            <div style="text-align: center;">
                <div class="user-avatar" style="width: 120px; height: 120px; font-size: 3rem; margin: 0 auto;">
                    {user["nombre"][0].upper()}
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3 style="color: #0A2463; margin-bottom: 1rem;">{user["nombre"]}</h3>
                <p><strong>Email:</strong> {user["email"]}</p>
                <p><strong>Teléfono:</strong> {user["telefono"]}</p>
                <p><strong>ID:</strong> <code>{user["id"][:8]}...</code></p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("### 📊 Análisis de Mi Historial")

    if st.session_state.graphrag.is_available():
        patterns = st.session_state.graphrag.analyze_incident_patterns(user["id"])

        if patterns.get("total_incidents", 0) > 0:
            st.markdown(
                f"**Total de incidentes analizados:** {patterns['total_incidents']}"
            )

            if patterns.get("incident_types"):
                st.markdown("**Tipos de incidentes reportados:**")
                for tipo, count in patterns["incident_types"].items():
                    st.markdown(f"- {tipo}: {count}")

            if patterns.get("recommendations"):
                st.markdown("### 💡 Recomendaciones")
                for rec in patterns["recommendations"]:
                    st.info(rec)
        else:
            st.info("No hay suficientes datos para análisis. Reporta más incidentes.")
    else:
        st.warning(
            "GraphRAG no disponible. Configure ZEP_API_KEY para análisis avanzado."
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    if st.button("🚪 Cerrar Sesión", type="primary", use_container_width=True):
        st.session_state.user = None
        st.session_state.current_page = "login"
        st.rerun()


def render_settings():
    apply_custom_styles()

    st.markdown("### ⚙️ Configuración")

    st.markdown(
        """
        <div class="metric-card">
            <h4 style="color: #0A2463;">Configuración de SAFE</h4>
            <p>La aplicación está configurada para Streamlit Cloud</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Variables de Entorno")
    st.code("""
# Para GraphRAG con Zep Cloud
ZEP_API_KEY=tu_api_key_aqui
    """)

    st.markdown("#### Características")
    st.markdown("""
    - ✅ Autenticación de usuarios
    - ✅ Registro de incidentes
    - ✅ Dashboard de métricas
    - ✅ Integración GraphRAG con Zep
    - ✅ Visualización de alertas
    - ✅ Análisis de patrones
    """)


def main():
    init_session_state()
    apply_custom_styles()

    if not st.session_state.user:
        if st.session_state.current_page == "register":
            render_register_form()
        else:
            render_login_form()
    else:
        show_bottom_nav(st.session_state.current_page, True)

        pages = {
            "home": render_home,
            "alerts": render_alerts,
            "incidents": render_incidents,
            "profile": render_profile,
            "settings": render_settings,
        }

        if st.session_state.current_page in pages:
            pages[st.session_state.current_page]()
        else:
            render_home()


if __name__ == "__main__":
    main()
